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

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

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


def search_similar_bugs(query, top_k=3):

    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    index = faiss.read_index(
        INDEX_FILE
    )

    data = pd.read_pickle(
        METADATA_FILE
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in range(len(indices[0])):

        index_number = indices[0][i]

        if index_number < len(data):

            result = {
                "bug_id": data.iloc[index_number]["bug_id"],
                "source": data.iloc[index_number]["source"],
                "chunk_type": data.iloc[index_number]["chunk_type"],
                "text": data.iloc[index_number]["text"],
                "distance": float(distances[0][i])
            }

            results.append(result)

    return results


if __name__ == "__main__":

    create_vector_store()

    query = "Application crashes because of NullPointerException"

    results = search_similar_bugs(
        query,
        top_k=3
    )

    print("\nSimilar Historical Bugs:\n")

    for result in results:

        print("Bug ID:", result["bug_id"])
        print("Source:", result["source"])
        print("Type:", result["chunk_type"])
        print("Text:", result["text"])
        print("Distance:", result["distance"])
        print("-" * 50)