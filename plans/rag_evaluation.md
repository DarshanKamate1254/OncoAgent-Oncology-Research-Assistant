# Task Plan: Ragas RAG Evaluation Integration

- **Status**: `Approved`
- **Date**: 2026-06-14
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [ ] **Dependency Update**: Add `ragas` to `backend/requirements.txt` and install
- [ ] **Evaluation Script**: Create `/backend/rag/evaluate.py` (under 70 lines) containing the Ragas evaluation logic
- [ ] **Verification**: Run evaluation with dummy or real dataset and output score results
- [ ] **Completion**: Update plan status to Completed and summarize task

---

## 1. Objective & Requirements
Implement an on-demand evaluation suite using the **Ragas** framework to compute metrics such as:
- **Faithfulness**: Whether the answer is grounded in the retrieved context.
- **Answer Relevance**: Whether the answer addresses the user query.
- **Context Precision**: Whether the retrieved context is relevant.
All evaluations will use OpenAI (`gpt-4o-mini` or similar) as the LLM evaluator.
Following the project's design guidelines, these expensive evaluations will be run as an **on-demand script** (`backend/rag/evaluate.py`) rather than block the live request loop.
The evaluation script must adhere to the **70-line limit**.

---

## 2. Proposed Changes

### ⚙️ Evaluation Script (`/backend/rag/evaluate.py`)
```python
import os
from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_precision
from advisor import get_clinical_response
from tools.rag_retriever import retrieve_clinical_guidelines

load_dotenv()

def run_ragas_evaluation():
    print("🧪 Running Ragas Evaluation...")
    
    # 1. Define evaluation dataset (test queries and ground truths)
    test_cases = [
        {
            "question": "What is the list of cancer types?",
            "ground_truth": "Cancers are classified into carcinomas, sarcomas, lymphomas/leukemias, germ cell tumors, and blastomas. There are over 200 known types."
        }
    ]
    
    # 2. Generate agent answers and retrieve contexts
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    for case in test_cases:
        q = case["question"]
        print(f"  Evaluating query: '{q}'")
        
        # Call RAG tool directly to get retrieved contexts
        retrieved_text = retrieve_clinical_guidelines.invoke(q)
        # Call agent to get response
        agent_ans = get_clinical_response(q)
        
        questions.append(q)
        answers.append(agent_ans)
        contexts.append([retrieved_text])
        ground_truths.append(case["ground_truth"])
        
    # 3. Create dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)
    
    # 4. Evaluate using Ragas
    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevance, context_precision]
    )
    
    print("\n📈 --- Ragas Evaluation Scores ---")
    for metric, score in result.items():
        print(f"{metric.capitalize()}: {score:.4f}")
    print("----------------------------------\n")

if __name__ == "__main__":
    run_ragas_evaluation()
```

---

## 3. Verification & Testing Plan
- [ ] Install `ragas`.
- [ ] Run `python rag/evaluate.py`.
- [ ] Verify that Ragas evaluates the question, calls OpenAI, and prints out scores (0.0 to 1.0) for the metrics.

---

## 4. User Sign-Off
- [ ] **User Approval**: *(Please let me know if you approve this plan to proceed!)*
