from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divides two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

tools = [add, subtract, multiply, divide]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001").bind_tools(tools)


def process(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content = "You are my AI assistant. Try to answer my query to the best of your knowledge.")
    response = llm.invoke([system_prompt] + state["messages"])
    return { "messages": state["messages"] + [response] }

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If the last message is a ToolMessage, go back to process
    if isinstance(last_message, ToolMessage):
        return "continue"
    # If the last message is an LLM response and has tool_calls, go to tools
    tool_calls = getattr(last_message, "tool_calls", None)
    if tool_calls:
        return "continue"
    # Otherwise, end
    return "end"
    
graph = StateGraph(AgentState)
graph.add_node("process", process)

tool_node = ToolNode(tools = tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("process")

graph.add_conditional_edges(
    "process",
    should_continue,
    {
        "continue": "tools",
        "end": END
    },
)

graph.add_edge("tools", "process")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = { "messages" : [HumanMessage(content="Add 5 and 3 and then multiply the result by 2. Also tell me 3 jokes.")]}

print_stream(app.stream(inputs, stream_mode="values"))


