import streamlit as st
import pandas as pd
from datetime import datetime
import os

from orchestrator.agent_orchestrator import diagnose_bug


def bug_submission_page():

    st.title("🐞 Intelligent Bug Diagnosis Platform")
    st.subheader("Bug Submission")

    title = st.text_input("Bug Title")

    description = st.text_area("Bug Description")

    stack_trace = st.text_area("Stack Trace")

    error_log = st.text_area("Error Log")

    uploaded_file = st.file_uploader(
        "Upload Bug Report / Log File",
        type=["txt", "log", "csv"]
    )

    if st.button("Submit Bug"):

        if title == "" or description == "":
            st.error("Bug title and description are required.")
            return

        os.makedirs("data/processed", exist_ok=True)

        # Read uploaded file
        file_content = ""

        if uploaded_file is not None:

            if uploaded_file.name.endswith(".csv"):

                uploaded_data = pd.read_csv(uploaded_file)

                file_content = uploaded_data.to_string()

            else:

                file_content = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

        # Create bug
        bug = {
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log
        }

        # Save bug
        bug_data = {
            "Bug ID": "BUG-" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log,
            "Uploaded File Content": file_content,
            "File Name": uploaded_file.name if uploaded_file else "",
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.DataFrame([bug_data])

        file_path = "data/processed/submitted_bugs.csv"

        if os.path.exists(file_path):

            df.to_csv(
                file_path,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                file_path,
                index=False
            )

        st.success("✅ Bug submitted successfully!")

        # Run diagnosis
        st.subheader("🔍 Bug Diagnosis")

        with st.spinner("Analyzing bug..."):

            result = diagnose_bug(bug)

        # Triage
        st.write("### 1️⃣ Triage")

        st.write(
            "Category:",
            result["Triage"]["category"]
        )

        st.write(
            "Severity:",
            result["Triage"]["severity"]
        )

        # Log analysis
        st.write("### 2️⃣ Log Analysis")

        for finding in result["Log Findings"]:

            st.write("•", finding)

        # Root cause
        st.write("### 3️⃣ Root Cause")

        st.info(result["Root Cause"])

        # Duplicate detection
        st.write("### 4️⃣ Similar Historical Bugs")

        duplicate_result = result["Duplicate Detection"]

        if duplicate_result["duplicate_found"]:

            st.warning("Similar historical bugs found.")

            for bug_result in duplicate_result["similar_bugs"]:

                st.write(
                    f"**{bug_result['bug_id']}** "
                    f"({bug_result['source']})"
                )

                st.write(
                    bug_result["text"]
                )

        else:

            st.success("No similar historical bugs found.")

        # Recommendation
        st.write("### 5️⃣ Recommended Fix")

        st.success(
            result["Recommended Fix"]
        )