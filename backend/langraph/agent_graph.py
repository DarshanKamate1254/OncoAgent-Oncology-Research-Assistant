import asyncio
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from agents.advisor import call_model, chat_model
from agents.critic import call_critic

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def route_critic(state: AgentState):
    last_msg = state["messages"][-1].content
    if "APPROVED" in last_msg.upper():
        return END
    return "advisor"

# Construct graph
workflow = StateGraph(AgentState)
workflow.add_node("advisor", call_model)
workflow.add_node("critic", call_critic)
workflow.add_edge(START, "advisor")
workflow.add_edge("advisor", "critic")
workflow.add_conditional_edges("critic", route_critic)
app_graph = workflow.compile()

async def get_clinical_response_stream(query: str):
    if not chat_model:
        yield "⚠️ OncoAgent: Model or API Key not configured."
        return
    try:
        async for event in app_graph.astream_events({"messages": [("user", query)]}, version="v2"):
            if event["event"] == "on_chat_model_stream" and event["metadata"].get("langgraph_node") == "advisor":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    yield chunk.content
    except Exception as e:
        yield f"⚠️ OncoAgent API Error: {str(e)}"

def get_clinical_response(query: str) -> str:
    async def collect():
        return "".join([c async for c in get_clinical_response_stream(query)])
    return asyncio.run(collect())
