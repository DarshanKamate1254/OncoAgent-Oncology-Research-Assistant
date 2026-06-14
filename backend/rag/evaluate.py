import os
import sys
from dotenv import load_dotenv

load_dotenv()

from datasets import Dataset
from openai import OpenAI

# Ensure backend directory is in the Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragas import evaluate
from ragas.llms import llm_factory
from ragas.embeddings import OpenAIEmbeddings
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from advisor import get_clinical_response
from tools.rag_retriever import retrieve_clinical_guidelines

def run_ragas_evaluation():
    print("🧪 Running Ragas Evaluation...")
    
    # 1. Initialize Ragas evaluator LLM and Embeddings using OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    evaluator_llm = llm_factory("gpt-4o-mini", client=client)
    evaluator_embeddings = OpenAIEmbeddings(client=client)
    
    # 2. Configure metrics properties
    faithfulness.llm = evaluator_llm
    answer_relevancy.llm = evaluator_llm
    answer_relevancy.embeddings = evaluator_embeddings
    context_precision.llm = evaluator_llm
    
    # 3. Define test cases
    test_cases = [
        {
            "question": "What is the list of cancer types?",
            "ground_truth": "Cancers are classified into carcinomas, sarcomas, lymphomas/leukemias, germ cell tumors, and blastomas."
        }
    ]
    
    questions, answers, contexts, ground_truths = [], [], [], []
    for case in test_cases:
        q = case["question"]
        print(f"  Evaluating query: '{q}'")
        retrieved_text = retrieve_clinical_guidelines.invoke(q)
        agent_ans = get_clinical_response(q)
        
        questions.append(q)
        answers.append(agent_ans)
        contexts.append([retrieved_text])
        ground_truths.append(case["ground_truth"])
        
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
        metrics=[faithfulness, answer_relevancy, context_precision]
    )
    
    print("\n📈 --- Ragas Evaluation Scores ---")
    for metric, score in result.items():
        print(f"{metric.capitalize()}: {score:.4f}")
    print("----------------------------------\n")

if __name__ == "__main__":
    run_ragas_evaluation()
