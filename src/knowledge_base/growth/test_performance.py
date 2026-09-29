import os
import sys
import time
import faiss

# Add the project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.knowledge_base.vector_store import search_similar_bugs


INDEX_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "vector_store",
    "bug_index.faiss"
)


def test_retrieval_performance():
    print("\n===== KNOWLEDGE BASE PERFORMANCE TEST =====")

    # Load FAISS index
    index = faiss.read_index(INDEX_FILE)

    # Display Knowledge Base size
    print("Knowledge Base vectors:", index.ntotal)

    # Test query
    query = """
    Application crashes when user login session is missing.
    NullPointerException occurs while accessing the user session.
    """

    # Measure retrieval time
    start_time = time.perf_counter()

    results = search_similar_bugs(query, top_k=5)

    end_time = time.perf_counter()

    processing_time = end_time - start_time

    print("Retrieved results:", len(results))
    print(f"Search processing time: {processing_time:.4f} seconds")

    print("\nTop Retrieved Bugs:")

    for i, result in enumerate(results, start=1):
        print(
            f"{i}. {result['bug_id']} | "
            f"Similarity: {result['similarity']}"
        )


if __name__ == "__main__":
    test_retrieval_performance()