import pandas as pd
import numpy as np
import faiss
import os

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

INDEX_FILE = "data/processed/vector_store/bug_index.faiss"

METADATA_FILE = "data/processed/vector_store/bug_metadata.pkl"


def create_vector_store():

    data = pd.read_pickle(
        "data/processed/bug_embeddings.pkl"
    )

    embeddings = np.array(
        data["embedding"].tolist()
    ).astype("float32")

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner Product on normalized vectors = Cosine Similarity
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    os.makedirs(
        "data/processed/vector_store",
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_FILE
    )

    data.to_pickle(
        METADATA_FILE
    )

    print("Vector store created successfully.")
    print("Total vectors:", index.ntotal)


def search_similar_bugs(query, top_k=5):

    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # Normalize query for cosine similarity
    faiss.normalize_L2(query_embedding)

    index = faiss.read_index(
        INDEX_FILE
    )

    data = pd.read_pickle(
        METADATA_FILE
    )

    similarities, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in range(len(indices[0])):

        index_number = indices[0][i]

        if index_number < 0:
            continue

        if index_number < len(data):

            similarity = float(
                similarities[0][i]
            )

            # Keep similarity between 0 and 1
            similarity = max(
                0.0,
                min(1.0, similarity)
            )

            result = {

                "bug_id":
                    data.iloc[index_number]["bug_id"],

                "source":
                    data.iloc[index_number]["source"],

                "chunk_type":
                    data.iloc[index_number]["chunk_type"],

                "text":
                    data.iloc[index_number]["text"],

                "similarity":
                    round(similarity, 4)

            }

            results.append(result)

    return results


if __name__ == "__main__":

    create_vector_store()

    query = (
        "Application crashes because of "
        "NullPointerException during login"
    )

    results = search_similar_bugs(
        query,
        top_k=3
    )

    print("\nSimilar Historical Bugs:\n")

    for result in results:

        print(
            "Bug ID:",
            result["bug_id"]
        )

        print(
            "Source:",
            result["source"]
        )

        print(
            "Type:",
            result["chunk_type"]
        )

        print(
            "Text:",
            result["text"]
        )

        print(
            "Similarity:",
            result["similarity"]
        )

        print("-" * 50)