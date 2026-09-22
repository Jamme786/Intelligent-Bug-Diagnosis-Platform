import streamlit as st
import pandas as pd
from datetime import datetime
import os

from orchestrator.agent_orchestrator import diagnose_bug


def bug_submission_page():

    st.title("🐞 Intelligent Bug Diagnosis Platform")
    st.subheader("Bug Submission")

    # =====================================================
    # BUG SUBMISSION FORM
    # =====================================================

    title = st.text_input("Bug Title")

    description = st.text_area("Bug Description")

    stack_trace = st.text_area("Stack Trace")

    error_log = st.text_area("Error Log")

    uploaded_file = st.file_uploader(
        "Upload Bug Report / Log File",
        type=["txt", "log", "csv"]
    )

    if st.button("Submit Bug"):

        # =================================================
        # VALIDATE INPUT
        # =================================================

        if title == "" or description == "":
            st.error("Bug title and description are required.")
            return

        os.makedirs("data/processed", exist_ok=True)

        # =================================================
        # READ UPLOADED FILE
        # =================================================

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

        # =================================================
        # CREATE BUG OBJECT
        # =================================================

        bug = {
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log
        }

        # =================================================
        # SAVE SUBMITTED BUG
        # =================================================

        bug_id = "BUG-" + datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )

        bug_data = {
            "Bug ID": bug_id,
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log,
            "Uploaded File Content": file_content,
            "File Name":
                uploaded_file.name
                if uploaded_file
                else "",
            "Submission Date":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
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

        # =================================================
        # ORIGINAL SUBMISSION
        # =================================================

        st.subheader("📄 Submitted Bug")

        with st.expander(
            "View Original Bug Report",
            expanded=True
        ):

            st.write("**Bug ID:**", bug_id)

            st.write("**Title:**", title)

            st.write(
                "**Description:**",
                description
            )

            st.write(
                "**Stack Trace:**",
                stack_trace
                if stack_trace
                else "Not provided"
            )

            st.write(
                "**Error Log:**",
                error_log
                if error_log
                else "Not provided"
            )

            if uploaded_file:

                st.write(
                    "**Uploaded File:**",
                    uploaded_file.name
                )

        # =================================================
        # RUN COMPLETE DIAGNOSIS
        # =================================================

        st.subheader("🔍 Complete Bug Diagnosis")

        with st.spinner(
            "Running Triage, Log Analysis, Root Cause, "
            "Duplicate Detection and Remediation..."
        ):

            result = diagnose_bug(bug)

        # =================================================
        # 1. TRIAGE
        # =================================================

        st.markdown("---")

        st.write("## 1️⃣ Triage Analysis")

        triage = result.get(
            "Triage",
            {}
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Severity",
                triage.get(
                    "severity",
                    "Unknown"
                )
            )

        with col2:

            st.metric(
                "Priority",
                triage.get(
                    "priority",
                    "Unknown"
                )
            )

        with col3:

            st.metric(
                "Component",
                triage.get(
                    "component",
                    "Unknown"
                )
            )

        st.write(
            "**Confidence:**",
            triage.get(
                "confidence",
                0.0
            )
        )

        with st.expander(
            "Triage Reasoning",
            expanded=True
        ):

            st.write(
                triage.get(
                    "reasoning",
                    "No reasoning available."
                )
            )

        # =================================================
        # 2. LOG ANALYSIS
        # =================================================

        st.markdown("---")

        st.write("## 2️⃣ Log Analysis")

        log_result = result.get(
            "Log Findings",
            {}
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Exception Type:**",
                log_result.get(
                    "exception_type",
                    "Not Available"
                )
            )

        with col2:

            st.write(
                "**Confidence:**",
                log_result.get(
                    "confidence",
                    0.0
                )
            )

        st.write(
            "**Error Message:**",
            log_result.get(
                "error_message",
                "Not Available"
            )
        )

        failure_point = log_result.get(
            "failure_point",
            {}
        )

        with st.expander(
            "Failure Point",
            expanded=True
        ):

            st.write(
                "**File:**",
                failure_point.get(
                    "file",
                    "Not Available"
                )
            )

            st.write(
                "**Class:**",
                failure_point.get(
                    "class",
                    "Not Available"
                )
            )

            st.write(
                "**Method:**",
                failure_point.get(
                    "method",
                    "Not Available"
                )
            )

            st.write(
                "**Line:**",
                failure_point.get(
                    "line",
                    "Not Available"
                )
            )

        code_path = log_result.get(
            "code_path",
            []
        )

        with st.expander("Code Path"):

            if code_path:

                st.write(
                    " → ".join(code_path)
                )

            else:

                st.write("Not Available")

        # =================================================
        # 3. ROOT CAUSE
        # =================================================

        st.markdown("---")

        st.write("## 3️⃣ Root Cause Analysis")

        root_cause = result.get(
            "Root Cause",
            {}
        )

        root_cause_text = root_cause.get(
            "root_cause",
            "Root cause analysis unavailable."
        )

        confidence = root_cause.get(
            "confidence",
            0.0
        )

        evidence_available = root_cause.get(
            "evidence_available",
            False
        )

        st.info(
            "🎯 " + root_cause_text
        )

        st.write(
            "**Confidence:**",
            confidence
        )

        st.write(
            "**Failure Point:**",
            root_cause.get(
                "failure_point",
                "Not Available"
            )
        )

        with st.expander(
            "Reasoning",
            expanded=True
        ):

            st.write(
                root_cause.get(
                    "reasoning",
                    "No reasoning available."
                )
            )

        # Evidence status

        if evidence_available:

            st.success(
                "📚 Supporting historical evidence is available."
            )

        else:

            st.warning(
                "⚠️ Insufficient historical evidence."
            )

        # Supporting evidence

        supporting_evidence = root_cause.get(
            "supporting_evidence",
            []
        )

        if supporting_evidence:

            with st.expander(
                "Supporting Historical Evidence"
            ):

                for evidence in supporting_evidence:

                    st.write(
                        "**Bug ID:**",
                        evidence.get(
                            "bug_id",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Similarity:**",
                        evidence.get(
                            "similarity_percentage",
                            evidence.get(
                                "similarity_score",
                                "N/A"
                            )
                        )
                    )

                    st.write(
                        "**Historical Text:**",
                        evidence.get(
                            "historical_text",
                            "Not Available"
                        )
                    )

                    st.write(
                        "**Source:**",
                        evidence.get(
                            "source",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Evidence Explanation:**",
                        evidence.get(
                            "explanation",
                            "Not Available"
                        )
                    )

                    st.markdown("---")

        # =================================================
        # 4. DUPLICATE DETECTION
        # =================================================

        st.markdown("---")

        st.write("## 4️⃣ Duplicate Detection")

        duplicate_result = result.get(
            "Duplicate Detection",
            {}
        )

        duplicate_status = duplicate_result.get(
            "duplicate_status",
            "New/Unmatched"
        )

        duplicate_found = duplicate_result.get(
            "duplicate_found",
            False
        )

        match_count = duplicate_result.get(
            "match_count",
            0
        )

        if duplicate_found:

            st.warning(
                "🔄 Similar historical bugs detected."
            )

        else:

            st.success(
                "🆕 No likely duplicate found."
            )

        st.write(
            "**Detection Status:**",
            duplicate_status
        )

        st.write(
            "**Matches Analyzed:**",
            match_count
        )

        matching_bugs = duplicate_result.get(
            "matching_bugs",
            []
        )

        if matching_bugs:

            with st.expander(
                "View Historical Bug Matches",
                expanded=True
            ):

                for index, match in enumerate(
                    matching_bugs,
                    start=1
                ):

                    st.write(
                        f"### Match {index}"
                    )

                    st.write(
                        "**Bug ID:**",
                        match.get(
                            "bug_id",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Source:**",
                        match.get(
                            "source",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Similarity:**",
                        str(
                            match.get(
                                "similarity_percentage",
                                "N/A"
                            )
                        ) + "%"
                    )

                    st.write(
                        "**Classification:**",
                        match.get(
                            "status",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Historical Record:**",
                        match.get(
                            "historical_text",
                            "Not Available"
                        )
                    )

                    st.write(
                        "**Explanation:**",
                        match.get(
                            "explanation",
                            "Not Available"
                        )
                    )

                    st.write(
                        "**Resolution:**",
                        match.get(
                            "resolution",
                            "Not Available"
                        )
                    )

                    st.markdown("---")

        # =================================================
        # 5. REMEDIATION
        # =================================================

        st.markdown("---")

        st.write("## 5️⃣ Remediation Recommendation")

        remediation = result.get(
            "Recommended Fix",
            {}
        )

        recommended_fix = remediation.get(
            "recommended_fix",
            "No recommendation available."
        )

        implementation_guidance = remediation.get(
            "implementation_guidance",
            "No implementation guidance available."
        )

        remediation_confidence = remediation.get(
            "confidence",
            0.0
        )

        evidence_type = remediation.get(
            "evidence_type",
            "Unknown"
        )

        if evidence_type == "Insufficient Evidence":

            st.warning(
                "⚠️ Insufficient Evidence"
            )

        else:

            st.success(
                "🛠️ Recommended Fix"
            )

        st.info(
            recommended_fix
        )

        st.write(
            "**Confidence:**",
            remediation_confidence
        )

        st.write(
            "**Evidence Type:**",
            evidence_type
        )

        with st.expander(
            "Implementation Guidance",
            expanded=True
        ):

            st.write(
                implementation_guidance
            )

        historical_evidence = remediation.get(
            "historical_evidence",
            []
        )

        if historical_evidence:

            with st.expander(
                "Historical Fix References"
            ):

                for evidence in historical_evidence:

                    st.write(
                        "**Bug ID:**",
                        evidence.get(
                            "bug_id",
                            "Unknown"
                        )
                    )

                    st.write(
                        "**Similarity:**",
                        evidence.get(
                            "similarity_percentage",
                            evidence.get(
                                "similarity_score",
                                "N/A"
                            )
                        )
                    )

                    st.write(
                        "**Historical Evidence:**",
                        evidence.get(
                            "historical_text",
                            "Not Available"
                        )
                    )

                    st.write(
                        "**Source:**",
                        evidence.get(
                            "source",
                            "Unknown"
                        )
                    )

                    st.markdown("---")

        # =================================================
        # FINAL SUMMARY
        # =================================================

        st.markdown("---")

        st.write("## 📊 Diagnosis Summary")

        summary_data = {

            "Severity":
                triage.get(
                    "severity",
                    "Unknown"
                ),

            "Priority":
                triage.get(
                    "priority",
                    "Unknown"
                ),

            "Component":
                triage.get(
                    "component",
                    "Unknown"
                ),

            "Root Cause Confidence":
                root_cause.get(
                    "confidence",
                    0.0
                ),

            "Duplicate Status":
                duplicate_status,

            "Remediation Confidence":
                remediation_confidence
        }

        summary_df = pd.DataFrame(
            [summary_data]
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        st.success(
            "✅ Complete structured bug diagnosis report generated."
        )