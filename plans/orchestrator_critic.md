# Task Plan: Orchestrator and Critic Agent Integration

- **Status**: `Completed`
- **Date**: 2026-06-14
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Advisor Agent Update**: Refactor `/backend/agents/advisor.py` to bind and execute tools internally (under 70 lines)
- [x] **Critic Agent**: Create `/backend/agents/critic.py` containing the Critic's prompt and node logic (under 70 lines)
- [x] **Orchestrator Routing**: Update `/backend/langraph/agent_graph.py` to compile the `START -> agent -> critic -> route` graph (under 70 lines)
- [x] **Verification**: Run local tests (via curl) to observe the multi-agent loop in action
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Multi-Agent Design
We will implement an Advisor-Critic multi-agent architecture orchestrated via LangGraph:
1. **Advisor (`agents.advisor`)**:
   - Generates/revises the clinical response draft.
   - Binds and executes tools (`retrieve_clinical_guidelines`) internally inside its node loop before returning the final draft message.
2. **Critic (`agents.critic`)**:
   - Reviews the clinical response draft.
   - Outputs `APPROVED` if it's correct. Otherwise, it outputs detailed revision feedback.
3. **Orchestrator (`langraph.agent_graph`)**:
   - Orchestrates the flow:
     - `START` -> `agent`
     - `agent` (draft completed) -> `critic`
     - `critic` -> if approved -> `END`
     - `critic` -> if not approved -> `agent` (for revision based on feedback)

---

## 2. Proposed Implementations

### 🕵️‍♂️ Critic Agent (`/backend/agents/critic.py`)
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage

load_dotenv()

CRITIC_PROMPT = (
    "You are a Clinical Critic. Your job is to review OncoAgent's response for clinical accuracy, "
    "conciseness, and compliance with clinical guidelines. "
    "If the draft response is accurate and formatted correctly, reply with ONLY the word: APPROVED. "
    "Otherwise, provide clear, constructive feedback on what needs to be changed. Do not write 'APPROVED' if changes are needed."
)

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

async def call_critic(state):
    # Retrieve only the last agent message to review
    agent_msg = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            agent_msg = msg.content
            break
            
    prompt = f"{CRITIC_PROMPT}\n\nDraft response to review:\n{agent_msg or 'No draft response found.'}"
    response = await chat_model.ainvoke([("user", prompt)])
    return {"messages": [response]}
```

---

## 3. User Sign-Off
- [ ] **User Approval**: *(Please let me know if you approve this plan to proceed!)*
