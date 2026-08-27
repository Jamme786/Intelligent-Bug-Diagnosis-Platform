import pandas as pd
import os


def create_chunks(input_file, output_file):

    print("Reading:", input_file)

    df = pd.read_csv(input_file)

    chunks = []

    for _, row in df.iterrows():

        text = (
            "Bug Description: " + str(row["description"]) +
            "\nSeverity: " + str(row["severity"]) +
            "\nPriority: " + str(row["priority"]) +
            "\nComponent: " + str(row["component"]) +
            "\nProduct: " + str(row["product"]) +
            "\nResolution: " + str(row["resolution"])
        )

        chunks.append({
            "bug_id": row["bug_id"],
            "project": row["project"],
            "text": text
        })

    result = pd.DataFrame(chunks)

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    result.to_csv(
        output_file,
        index=False
    )

    print("Chunks created:", len(result))
    print("Saved:", output_file)


if __name__ == "__main__":

    create_chunks(
        "data/processed/mozilla_historical_bugs.csv",
        "data/processed/mozilla_bug_chunks.csv"
    )

    create_chunks(
        "data/processed/eclipse_historical_bugs.csv",
        "data/processed/eclipse_bug_chunks.csv"
    )