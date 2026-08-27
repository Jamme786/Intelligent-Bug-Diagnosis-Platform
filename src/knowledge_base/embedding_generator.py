import pandas as pd
import os
from sentence_transformers import SentenceTransformer


def generate_embeddings(input_file, output_file):

    data = pd.read_csv(input_file)

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    texts = data["text"].astype(str).tolist()

    embeddings = model.encode(texts)

    data["embedding"] = embeddings.tolist()

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    data.to_pickle(output_file)

    print("Embeddings generated successfully.")
    print("Total embeddings:", len(embeddings))


if __name__ == "__main__":

    input_file = "data/processed/bug_chunks.csv"

    output_file = "data/processed/bug_embeddings.pkl"

    generate_embeddings(
        input_file,
        output_file
    )