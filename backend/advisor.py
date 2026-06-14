import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools.rag_retriever import retrieve_clinical_guidelines

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "You must search the local database using the retrieve_clinical_guidelines tool for ANY medical, cancer, "
    "or oncology-related questions. Do not answer from general knowledge if you can retrieve data. "
    "Provide clinical insights, targeted therapy guidelines, and trial matching. "
    "Use markdown (bolding, lists) to format your replies. if you do not find in our data say, you dont know. dont answer on your own"
)

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=api_key) if api_key else None
llm_with_tools = chat_model.bind_tools([retrieve_clinical_guidelines]) if chat_model else None

async def get_clinical_response_stream(query: str):
    if not llm_with_tools:
        yield "⚠️ OncoAgent: Model or API Key not configured."
        return
    try:
        messages = [("system", SYSTEM_PROMPT), ("human", query)]
        ai_msg = await llm_with_tools.ainvoke(messages)
        if ai_msg.tool_calls:
            tool_call = ai_msg.tool_calls[0]
            tool_query = tool_call["args"]["query"]
            context = retrieve_clinical_guidelines.invoke(tool_query)
            messages.append(ai_msg)
            messages.append({
                "role": "tool",
                "content": context,
                "tool_call_id": tool_call["id"]
            })
            async for chunk in chat_model.astream(messages):
                if chunk.content:
                    yield chunk.content
        else:
            yield ai_msg.content
    except Exception as e:
        yield f"⚠️ OncoAgent API Error: {str(e)}"

def get_clinical_response(query: str) -> str:
    async def collect():
        return "".join([c async for c in get_clinical_response_stream(query)])
    return asyncio.run(collect())
