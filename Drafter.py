from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os

load_dotenv()

document_content = ""

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str) -> str:
    """Updates the document content."""
    global document_content
    document_content = content
    return f"The document has been updated with the content: {content}"

@tool
def save(filename: str) -> str:
    """Saves the document content to a file."""
    global document_content

    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"

    try:
        with open(filename, "w") as file:
            file.write(document_content)
        return f"Document saved to {filename}"
    except Exception as e:
        return f"Error saving document: {str(e)}"

tools = [update, save]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=os.environ["GOOGLE_API_KEY"])


def process(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f""" 
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.

    The current document content is: {document_content}
    """) 
    
    if not state["messages"]:
        user_input = "I'm ready to help you update a document. What would you like to create?"
    else:
        user_input = input("\nWhat would you like to do with the document? ")

    user_message = HumanMessage(content=user_input)
    all_messages = [system_prompt] + state["messages"] + [user_message]

    response = llm.invoke(all_messages)

    print(f"\n🤖 AI : {response.content}")

    if(hasattr(response, "tool_calls") and response.tool_calls):
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) ->str:
    """Determine if we should continue or end the conversation."""

    messages = state["messages"]

    if not messages:
        return "continue"
    
    for message in reversed(messages):
        # Check all message types for the exit keywords
        if hasattr(message, "content") and \
           "saved" in message.content.lower() and \
           "document" in message.content.lower():
            return "end"
         
    return "continue"

def print_messages(messages):
    """Print the messages in a more readable format."""

    if not messages:
         return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")

graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("process")

graph.add_edge("process", "tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "process",
        "end": END
    },
)
    
app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()
