# OncoAgent: Gen AI Pillars Audit & Roadmap

This document provides a detailed overview of the OncoAgent architecture, audits the project against the 10 Gen AI Pillars shown in the mind map, and highlights the implementation steps required to elevate the system to a production-ready standard.

---

## 1. Executive Summary: 5 Points About OncoAgent

1. **Structured Multi-Agent Architecture**: OncoAgent uses a LangGraph-based **Advisor-Critic** loop ([agent_graph.py](file:///d:/projects/cancer_agents/cancer-agent/backend/langraph/agent_graph.py)). The `Advisor` agent acts as the generator, utilizing retrieved clinical trials and notes to draft a response. The `Clinical Critic` agent acts as a guardrail, evaluating drafts for clinical compliance and either approving them or routing them back to the Advisor with feedback.
2. **Context-Aware Local RAG**: The core database pipeline is built using **LlamaIndex** and **ChromaDB** ([pipeline.py](file:///d:/projects/cancer_agents/cancer-agent/backend/rag/pipeline.py)). Uploaded research papers, clinical trial definitions, or oncology guidelines are parsed, split, embedded via OpenAI's `text-embedding-3-small` model, and cached in a local vector database.
3. **Structured Evaluation Harness**: The project includes a dedicated assessment script ([evaluate.py](file:///d:/projects/cancer_agents/cancer-agent/backend/rag/evaluate.py)) running **Ragas**. It scores the RAG retrieval and generation accuracy across three dimensions: *Faithfulness*, *Answer Relevancy*, and *Context Precision*.
4. **Next.js App Router Frontend**: The user interface is built with React 18, Next.js (App Router), and TypeScript. In compliance with the project instructions, styling is implemented using Vanilla CSS Modules (`*.module.css`) to maintain a premium, dark/neon theme with custom layouts.
5. **Real-time Event Streaming & Document Sync**: The frontend communicating with FastAPI uses **Server-Sent Events (SSE)** to stream agent thoughts to the user ([page.tsx](file:///d:/projects/cancer_agents/cancer-agent/frontend/src/app/page.tsx)). It also includes a **Document Center** tab allowing researchers to upload clinical files and trigger database parsing in real time.

---

## 2. Gen AI Pillars: Current Status & Gap Analysis

Based on the 10 core pillars of Gen AI development, here is the current audit of OncoAgent:

| Mind Map Gen AI Pillar | Status in Codebase | Gap / Remaining Work |
| :--- | :--- | :--- |
| **RAG** | **Implemented** | Basic vector-based semantic search works. |
| **Agent / Multi Agent** | **Implemented** | LangGraph handles a two-agent state machine. |
| **Evaluation** | **Partially Implemented** | `evaluate.py` runs Ragas, but has only 1 hardcoded test case and is offline. |
| **Explainability** | **Missing** | Answers lack inline source citations or matching confidence scores in the UI. |
| **Cost Management** | **Missing** | No token calculators or cost telemetry exist in backend/frontend. |
| **Context Engineering** | **Minimal** | Basic cosine similarity top-3. Lacks hybrid keyword/dense search and reranking. |
| **Observability** | **Missing** | No active framework tracing (e.g., LangSmith, LangFuse, OpenTelemetry) is active. |
| **Guardrails** | **Weak** | No active query parsing/filtering or post-generation validation layers. |
| **Tools / MCP** | **Minimal** | Only a single local DB lookup tool. No active internet/PubMed tools or MCP servers. |
| **Fine Tuning** | **Missing** | No collection pipelines for approved agent/critic text pairs. |

---

## 3. Implementation Blueprint: What to Add & Where

To implement the missing components, follow this development map:

### 🔍 1. Explainability: RAG Source Citations
* **What to add**: Retain source documents (filename, text snippet, similarity score) from ChromaDB in the LangGraph state and render them in the UI.
* **Where to add**:
  * **Backend**:
    1. Update the state dictionary in [agent_graph.py](file:///d:/projects/cancer_agents/cancer-agent/backend/langraph/agent_graph.py) to declare a list for sources.
    2. Modify [advisor.py](file:///d:/projects/cancer_agents/cancer-agent/backend/agents/advisor.py) to capture tool outputs and return them in the agent response.
  * **Frontend**:
    1. In [page.tsx](file:///d:/projects/cancer_agents/cancer-agent/frontend/src/app/page.tsx), parse sources from the API response payload and render them as expandable card components under the message text.

### 💰 2. Cost Management: Token and API Telemetry
* **What to add**: Count the prompt and completion tokens for the query/retrieval cycles using `tiktoken` or LangChain's callback wrappers.
* **Where to add**:
  * **Backend**:
    1. Create `backend/tools/cost_calculator.py` to map API models to their respective dollar costs.
    2. Hook this helper into the `api/chat` route of [main.py](file:///d:/projects/cancer_agents/cancer-agent/backend/main.py) to return a token budget report inside the event stream.
  * **Frontend**:
    1. Display a telemetry status bar in [page.tsx](file:///d:/projects/cancer_agents/cancer-agent/frontend/src/app/page.tsx) rendering session token counts and costs (e.g., `Session Cost: $0.0018`).

### 🧬 3. Context Engineering: Hybrid Search & Reranking
* **What to add**: Replace simple similarity search with hybrid search (dense embeddings + BM25 keyword matching) and apply a reranking filter (like FlashRank or Cohere).
* **Where to add**:
  * **Backend**:
    1. In [vector_store.py](file:///d:/projects/cancer_agents/cancer-agent/backend/rag/vector_store.py) and [rag_retriever.py](file:///d:/projects/cancer_agents/cancer-agent/backend/tools/rag_retriever.py), configure LlamaIndex to run hybrid retrieval.
    2. In `backend/tools/rag_retriever.py`, insert a `NodePostprocessor` (reranker) to filter the top 10 retrieved chunks down to the 3 most contextually relevant guidelines.

### 🛡️ 4. Guardrails: Safety Verification
* **What to add**: Block requests containing non-oncological topics, inappropriate inputs, or requests to bypass medical safety guidelines.
* **Where to add**:
  * **Backend**:
    1. Implement a router/validator node in [agent_graph.py](file:///d:/projects/cancer_agents/cancer-agent/backend/langraph/agent_graph.py) before the `Advisor` node (e.g., `backend/agents/guardrails.py`).
    2. Program this node to run check classifications and abort immediately with a friendly warning if the safety rules are violated.

### 🔌 5. Tools / MCP: External Clinical Repositories
* **What to add**: Allow the Advisor agent to fetch clinical trials directly from public APIs when local search returns no results.
* **Where to add**:
  * **Backend**:
    1. Create a search tool `backend/tools/clinical_trials_api.py` that queries standard open APIs (e.g., ClinicalTrials.gov REST interface).
    2. Bind this tool to the Advisor model in [advisor.py](file:///d:/projects/cancer_agents/cancer-agent/backend/agents/advisor.py).

### 📈 6. Observability: Run Tracing
* **What to add**: Connect the LangGraph system to a tracking framework to visualize graph executions and log durations.
* **Where to add**:
  * **Backend**: Enable environment keys in `backend/.env` (e.g. `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_PROJECT="oncoagent"`).
