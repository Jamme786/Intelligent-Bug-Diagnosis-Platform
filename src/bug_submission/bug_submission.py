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

        # -------------------------------------------------
        # Validate Input
        # -------------------------------------------------

        if title == "" or description == "":
            st.error("Bug title and description are required.")
            return

        os.makedirs("data/processed", exist_ok=True)

        # -------------------------------------------------
        # Read Uploaded File
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Create Bug
        # -------------------------------------------------

        bug = {
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log
        }

        # -------------------------------------------------
        # Save Bug
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Run Diagnosis
        # -------------------------------------------------

        st.subheader("🔍 Bug Diagnosis")

        with st.spinner("Analyzing bug..."):

            result = diagnose_bug(bug)

        # =================================================
        # 1. TRIAGE AGENT
        # =================================================

        st.write("### 1️⃣ Triage")

        triage = result["Triage"]

        st.write(
            "Severity:",
            triage["severity"]
        )

        st.write(
            "Priority:",
            triage["priority"]
        )

        st.write(
            "Affected Component:",
            triage["component"]
        )

        st.write(
            "Confidence:",
            triage["confidence"]
        )

        st.write(
            "Reasoning:",
            triage["reasoning"]
        )

        # =================================================
        # 2. LOG ANALYSIS AGENT
        # =================================================

        st.write("### 2️⃣ Log Analysis")

        log_result = result["Log Findings"]

        st.write(
            "Exception Type:",
            log_result["exception_type"]
        )

        st.write(
            "Error Message:",
            log_result["error_message"]
        )

        # Failure Point

        failure_point = log_result["failure_point"]

        st.write(
            "File:",
            failure_point["file"]
        )

        st.write(
            "Class:",
            failure_point["class"]
        )

        st.write(
            "Method:",
            failure_point["method"]
        )

        st.write(
            "Line:",
            failure_point["line"]
        )

        # Code Path

        if log_result["code_path"]:

            code_path = " → ".join(
                log_result["code_path"]
            )

        else:

            code_path = "Not Available"

        st.write(
            "Code Path:",
            code_path
        )

        st.write(
            "Confidence:",
            log_result["confidence"]
        )

        # =================================================
        # 3. ROOT CAUSE
        # =================================================

        st.write("### 3️⃣ Root Cause")

        st.info(
            result["Root Cause"]
        )

        # =================================================
        # 4. DUPLICATE DETECTION
        # =================================================

        st.write("### 4️⃣ Similar Historical Bugs")

        duplicate_result = result["Duplicate Detection"]

        if duplicate_result["duplicate_found"]:

            st.warning(
                "Similar historical bugs found."
            )

            for bug_result in duplicate_result["similar_bugs"]:

                st.write(
                    f"**{bug_result['bug_id']}** "
                    f"({bug_result['source']})"
                )

                st.write(
                    bug_result["text"]
                )

        else:

            st.success(
                "No similar historical bugs found."
            )

        # =================================================
        # 5. RECOMMENDED FIX
        # =================================================

        st.write("### 5️⃣ Recommended Fix")

        st.success(
            result["Recommended Fix"]
        )
