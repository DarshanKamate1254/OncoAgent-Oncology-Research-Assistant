# Task Plan: Split Agent Logic from Graph Compilation

- **Status**: `Completed`
- **Date**: 2026-06-14
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Agent Directory**: Create `/backend/agents/` directory
- [x] **Agent Node Setup**: Create `/backend/agents/advisor.py` containing prompt, LLM setup, and node/routing functions (under 70 lines)
- [x] **Graph Setup**: Create `/backend/langraph/agent_graph.py` to define state, compile the graph, and provide response functions (under 70 lines)
- [x] **Imports Migration**: Update `/backend/main.py` and `/backend/rag/evaluate.py` to import from `langraph.agent_graph`
- [x] **Verification**: Run local tests (via curl) to ensure streaming works identically after refactoring
- [x] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Architecture
To follow clean agent separation principles, we will split the graph orchestration from the agent's logic:
1. **Agent Logic (`/backend/agents/advisor.py`)**:
   - Contains OncoAgent system prompt.
   - Instantiates ChatOpenAI model and binds tools.
   - Defines the node handlers: `call_model`, `call_tool`, and `route_agent`.
2. **Graph Orchestration (`/backend/langraph/agent_graph.py`)**:
   - Defines `AgentState`.
   - Imports node handlers from `agents.advisor`, builds, and compiles the `StateGraph` (`app_graph`).
   - Implements the response wrappers `get_clinical_response` and `get_clinical_response_stream`.
3. **fastapi and evaluate updates**:
   - Import directly from `langraph.agent_graph` instead of `langraph.advisor`.

This avoids circular module-level imports cleanly while ensuring both files remain small and maintainable (well below the 70 lines limit).

---

## 2. User Sign-Off
- [ ] **User Approval**: *(Please let me know if you approve this plan to proceed!)*
