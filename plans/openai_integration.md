# Task Plan: OpenAI Integration for Oncology Chatbot

- **Status**: `Completed`
- **Date**: 2026-06-13
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Dependency Update**: Add `openai` and `python-dotenv` to `requirements.txt` and install
- [x] **Backend Integration**: Update `advisor.py` to call OpenAI API using `OPENAI_API_KEY` (under 70 lines)
- [x] **Verification**: Validate functional API responses from OpenAI
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Connect the OncoAgent chatbot backend to OpenAI's GPT models using the `OPENAI_API_KEY` stored in `.env`.
- Ensure all backend code files remain strictly under the **70-line limit**.
- Load `.env` securely using `python-dotenv`.
- Set up a system prompt in OpenAI to instruct the model to behave as **OncoAgent**, a specialized clinical oncology research assistant.
- Provide a robust local fallback if the API call fails or the key is invalid.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [ ] `/backend/requirements.txt` – Add `openai` and `python-dotenv`.
- [ ] `/backend/advisor.py` – Load `.env`, initialize the OpenAI client, and request chat completions (keeping the file under 70 lines).

### ⚙️ Backend Implementation
Update `/backend/advisor.py` (approx. 50 lines total):
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

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
```

---

## 3. Verification & Testing Plan
- [ ] Install updated packages via `pip install -r requirements.txt`.
- [ ] Verify that query submissions hit the OpenAI completion endpoint and return dynamic responses.
- [ ] Ensure the file size of `advisor.py` is under 70 lines.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-13
