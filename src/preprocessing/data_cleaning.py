import pandas as pd
import os


def clean_dataset(input_file, output_file):

    print("Reading:", input_file)

    data = pd.read_csv(input_file)

    print("Original records:", len(data))

    # Remove duplicate records
    data = data.drop_duplicates()

    # Remove completely empty rows
    data = data.dropna(how="all")

    # Replace missing values
    data = data.fillna("")

    # Create output folder
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    # Save cleaned dataset
    data.to_csv(
        output_file,
        index=False
    )

    print("Cleaned records:", len(data))

    print("Saved:", output_file)


if __name__ == "__main__":

    datasets = {

        "Mozilla":
        (
            "data/raw/mozilla_bugs.csv",
            "data/processed/mozilla_cleaned.csv"
        ),

        "Apache":
        (
            "data/raw/apache_bugs.csv",
            "data/processed/apache_cleaned.csv"
        ),

        "Eclipse":
        (
            "data/raw/eclipse_bugs.csv",
            "data/processed/eclipse_cleaned.csv"
        )
    }

    for name, files in datasets.items():

        input_file = files[0]
        output_file = files[1]

        if os.path.exists(input_file):

            clean_dataset(
                input_file,
                output_file
            )

        else:

            print(
                name,
                "dataset not found."
            )