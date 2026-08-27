import json
import pandas as pd
import os


DATASET_PATH = (
    "msr2013-bug_dataset-master/"
    "msr2013-bug_dataset-master/data/v02"
)


def load_json_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def process_dataset(project):

    folder = os.path.join(DATASET_PATH, project)

    print("Processing:", project)

    short_desc = load_json_file(
        os.path.join(folder, "short_desc.json")
    )

    severity = load_json_file(
        os.path.join(folder, "severity.json")
    )

    priority = load_json_file(
        os.path.join(folder, "priority.json")
    )

    status = load_json_file(
        os.path.join(folder, "bug_status.json")
    )

    resolution = load_json_file(
        os.path.join(folder, "resolution.json")
    )

    component = load_json_file(
        os.path.join(folder, "component.json")
    )

    product = load_json_file(
        os.path.join(folder, "product.json")
    )

    data = []

    for bug_id in short_desc:

        data.append({
            "bug_id": bug_id,
            "project": project,
            "description": short_desc.get(bug_id, ""),
            "severity": severity.get(bug_id, ""),
            "priority": priority.get(bug_id, ""),
            "status": status.get(bug_id, ""),
            "resolution": resolution.get(bug_id, ""),
            "component": component.get(bug_id, ""),
            "product": product.get(bug_id, "")
        })

    df = pd.DataFrame(data)

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    output = (
        f"data/processed/"
        f"{project}_historical_bugs.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print(
        project,
        "records:",
        len(df)
    )

    print("Saved:", output)


if __name__ == "__main__":

    process_dataset("mozilla")
    process_dataset("eclipse")