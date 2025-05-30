from typing import List, TypedDict, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

def process(state: AgentState):
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"AI : {response.content}")
    print(f"CURRENT STATE: {state['messages']}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")

while(user_input != "exit"):
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")

with(open("logging.txt", "w")) as file:
    for message in conversation_history:
        if(isinstance(message, HumanMessage)):
            file.write(f"User: {message.content}\n")
        elif(isinstance(message, AIMessage)):
            file.write(f"AI: {message.content}\n")
print("Conversation logged to logging.txt")