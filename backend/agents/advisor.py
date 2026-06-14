import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from tools.rag_retriever import retrieve_clinical_guidelines

load_dotenv()

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "You must search the local database using the retrieve_clinical_guidelines tool for ANY medical, cancer, "
    "or oncology-related questions. Do not answer from general knowledge if you can retrieve data. "
    "Provide clinical insights, targeted therapy guidelines, and trial matching. "
    "Use markdown (bolding, lists) to format your replies. if you do not find in our data say, you dont know. dont answer on your own"
)

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
llm_with_tools = chat_model.bind_tools([retrieve_clinical_guidelines]) if chat_model else None

async def call_model(state):
    messages = [("system", SYSTEM_PROMPT)] + list(state["messages"])
    while True:
        response = await llm_with_tools.ainvoke(messages)
        if not response.tool_calls:
            return {"messages": [response]}
        messages.append(response)
        for tool_call in response.tool_calls:
            context = retrieve_clinical_guidelines.invoke(tool_call["args"]["query"])
            messages.append(ToolMessage(content=context, tool_call_id=tool_call["id"]))
