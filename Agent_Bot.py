from typing import List, TypedDict
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages : List[HumanMessage]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

def process(state: AgentState):
    response = llm.invoke(state["messages"])
    print(f"AI : {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

user_input = "Enter: "
while(user_input != "exit"):
    user_input = input("Enter : ")
    app.invoke({"messages": [HumanMessage(content=user_input)]})
