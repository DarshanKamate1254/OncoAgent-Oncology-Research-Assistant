import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_PROMPT = (
    "You are OncoAgent, a specialized oncology research assistant. "
    "Provide clinical insights, targeted therapy guidelines (e.g. EGFR, BRCA), "
    "and trial criteria matching. Be professional, structured, and medically accurate. "
    "Use markdown (bolding, lists) to format your replies."
)

def get_clinical_response(query: str) -> str:
    if not client:
        return "⚠️ OncoAgent: OpenAI client not configured. Please add OPENAI_API_KEY to your .env file."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content or "No response from AI."
    except Exception as e:
        return f"⚠️ OncoAgent API Error: {str(e)}"
