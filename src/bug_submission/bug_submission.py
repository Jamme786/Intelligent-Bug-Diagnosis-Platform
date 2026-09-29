import streamlit as st
import pandas as pd
from datetime import datetime
import os

from orchestrator.agent_orchestrator import diagnose_bug


def bug_submission_page():

    # =========================================================
    # PAGE CONFIGURATION
    # =========================================================

    st.set_page_config(
        page_title="Intelligent Bug Diagnosis Platform",
        page_icon="🐞",
        layout="wide"
    )

    # =========================================================
    # PROFESSIONAL UI STYLE
    # =========================================================

    st.markdown(
        """
        <style>

        .main {
            background-color: #0e1117;
        }

        .hero {
            background: linear-gradient(
                135deg,
                #151a25,
                #20283a
            );
            border: 1px solid #303746;
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 25px;
        }

        .hero-title {
            font-size: 34px;
            font-weight: 700;
        }

        .hero-subtitle {
            color: #aeb6c5;
            font-size: 16px;
            margin-top: 8px;
        }

        .section-title {
            font-size: 23px;
            font-weight: 650;
            margin-top: 20px;
            margin-bottom: 15px;
        }

        .card {
            background-color: #171b24;
            border: 1px solid #303746;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .card-title {
            font-size: 18px;
            font-weight: 650;
            margin-bottom: 10px;
        }

        .card-text {
            color: #c8ced9;
            line-height: 1.6;
        }

        .root-card {
            background-color: #182233;
            border-left: 5px solid #6c8cff;
            border-radius: 12px;
            padding: 22px;
            margin: 15px 0;
        }

        .root-label {
            color: #9da6b5;
            font-size: 13px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .root-text {
            font-size: 20px;
            font-weight: 600;
            line-height: 1.5;
        }

        .fix-card {
            background-color: #17251f;
            border: 1px solid #2d614b;
            border-radius: 14px;
            padding: 22px;
            margin: 15px 0;
        }

        .fix-title {
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .pipeline {
            display: flex;
            gap: 8px;
            margin: 15px 0 25px 0;
        }

        .pipeline-step {
            flex: 1;
            text-align: center;
            padding: 12px 5px;
            background-color: #171b24;
            border: 1px solid #303746;
            border-radius: 10px;
            font-size: 13px;
        }

        .pipeline-active {
            border-color: #6c8cff;
            background-color: #1d263b;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # HEADER
    # =========================================================

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                🐞 Intelligent Bug Diagnosis Platform
            </div>

            <div class="hero-subtitle">
                AI-assisted defect analysis • Root cause detection •
                Duplicate identification • Fix recommendation
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:

        st.markdown("## 🧭 Diagnosis Pipeline")

        st.markdown(
            """
            **01** 📝 Bug Submission

            **02** 🎯 Triage Analysis

            **03** 📋 Log Analysis

            **04** 🧠 Root Cause Analysis

            **05** 🔄 Duplicate Detection

            **06** 🛠️ Remediation
            """
        )

        st.divider()

        st.markdown("### ⚙️ System Status")

        st.success("Knowledge Base: Ready")
        st.success("Diagnosis Engine: Ready")
        st.success("Agent Orchestrator: Ready")

        st.divider()

        st.caption(
            "Infosys Springboard Batch 3\n\n"
            "Intelligent Bug Diagnosis Platform"
        )

    # =========================================================
    # BUG SUBMISSION
    # =========================================================

    st.markdown(
        '<div class="section-title">📥 Submit New Bug</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        col1, col2 = st.columns([2, 1])

        with col1:

            title = st.text_input(
                "Bug Title",
                placeholder="Example: Critical Login Crash"
            )

        with col2:

            uploaded_file = st.file_uploader(
                "Upload Bug Report / Log",
                type=["txt", "log", "csv"]
            )

        description = st.text_area(
            "Bug Description",
            placeholder=(
                "Describe the problem, expected behaviour "
                "and actual behaviour..."
            ),
            height=110
        )

        col1, col2 = st.columns(2)

        with col1:

            stack_trace = st.text_area(
                "Stack Trace",
                placeholder="Paste stack trace here...",
                height=150
            )

        with col2:

            error_log = st.text_area(
                "Error Log",
                placeholder="Paste application error log here...",
                height=150
            )

        submit = st.button(
            "🔍 Analyze Bug",
            type="primary",
            use_container_width=True
        )

    # =========================================================
    # PROCESS BUG
    # =========================================================

    if submit:

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if title.strip() == "" or description.strip() == "":
            st.error(
                "Bug title and description are required."
            )
            return

        # -----------------------------------------------------
        # CREATE DATA DIRECTORY
        # -----------------------------------------------------

        os.makedirs(
            "data/processed",
            exist_ok=True
        )

        # -----------------------------------------------------
        # READ UPLOADED FILE
        # -----------------------------------------------------

        file_content = ""

        if uploaded_file is not None:

            try:

                if uploaded_file.name.endswith(".csv"):

                    uploaded_data = pd.read_csv(
                        uploaded_file
                    )

                    file_content = uploaded_data.to_string()

                else:

                    file_content = uploaded_file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )

            except Exception as error:

                st.warning(
                    f"Could not read uploaded file: {error}"
                )

        # -----------------------------------------------------
        # CREATE BUG OBJECT
        # -----------------------------------------------------

        bug = {
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log
        }

        # -----------------------------------------------------
        # GENERATE BUG ID
        # -----------------------------------------------------

        bug_id = (
            "BUG-"
            + datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

        # -----------------------------------------------------
        # SAVE BUG
        # -----------------------------------------------------

        bug_data = {
            "Bug ID": bug_id,
            "Title": title,
            "Description": description,
            "Stack Trace": stack_trace,
            "Error Log": error_log,
            "Uploaded File Content": file_content,
            "File Name": (
                uploaded_file.name
                if uploaded_file
                else ""
            ),
            "Submission Date": (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        }

        df = pd.DataFrame([bug_data])

        file_path = (
            "data/processed/submitted_bugs.csv"
        )

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

        # =====================================================
        # RUN DIAGNOSIS
        # =====================================================

        with st.spinner(
            "Running complete AI diagnosis pipeline..."
        ):

            result = diagnose_bug(bug)

        st.success(
            f"✅ Bug {bug_id} submitted and analyzed successfully."
        )

        # =====================================================
        # DIAGNOSIS PIPELINE
        # =====================================================

        st.markdown(
            '<div class="section-title">🔬 Diagnosis Pipeline</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="pipeline">

                <div class="pipeline-step pipeline-active">
                    📝<br>Submission
                </div>

                <div class="pipeline-step pipeline-active">
                    🎯<br>Triage
                </div>

                <div class="pipeline-step pipeline-active">
                    📋<br>Log Analysis
                </div>

                <div class="pipeline-step pipeline-active">
                    🧠<br>Root Cause
                </div>

                <div class="pipeline-step pipeline-active">
                    🔄<br>Duplicate
                </div>

                <div class="pipeline-step pipeline-active">
                    🛠️<br>Remediation
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # EXTRACT RESULTS
        # =====================================================

        triage = result.get(
            "Triage",
            {}
        )

        log_result = result.get(
            "Log Findings",
            {}
        )

        root_cause = result.get(
            "Root Cause",
            {}
        )

        duplicate_result = result.get(
            "Duplicate Detection",
            {}
        )

        remediation = result.get(
            "Recommended Fix",
            {}
        )

        # =====================================================
        # OVERVIEW CARDS
        # =====================================================

        st.markdown(
            '<div class="section-title">📊 Diagnosis Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

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

        with col4:

            confidence = float(
                root_cause.get(
                    "confidence",
                    0
                )
            )

            st.metric(
                "Root Cause Confidence",
                f"{confidence * 100:.0f}%"
            )

        # =====================================================
        # TABS
        # =====================================================

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🎯 Triage",
                "📋 Log Analysis",
                "🧠 Root Cause",
                "🔄 Duplicate Detection",
                "🛠️ Remediation"
            ]
        )

        # =====================================================
        # TAB 1 - TRIAGE
        # =====================================================

        with tab1:

            st.markdown(
                "### 🎯 Triage Analysis"
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
                    "Affected Component",
                    triage.get(
                        "component",
                        "Unknown"
                    )
                )

            triage_confidence = float(
                triage.get(
                    "confidence",
                    0
                )
            )

            st.progress(
                min(triage_confidence, 1.0)
            )

            st.caption(
                f"Classification confidence: "
                f"{triage_confidence * 100:.0f}%"
            )

            with st.expander(
                "🔎 View Triage Reasoning"
            ):

                st.write(
                    triage.get(
                        "reasoning",
                        "No reasoning available."
                    )
                )

        # =====================================================
        # TAB 2 - LOG ANALYSIS
        # =====================================================

        with tab2:

            st.markdown(
                "### 📋 Log Analysis"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Exception Type",
                    log_result.get(
                        "exception_type",
                        "Not Available"
                    )
                )

            with col2:

                log_confidence = float(
                    log_result.get(
                        "confidence",
                        0
                    )
                )

                st.metric(
                    "Confidence",
                    f"{log_confidence * 100:.0f}%"
                )

            with col3:

                failure_point = log_result.get(
                    "failure_point",
                    {}
                )

                st.metric(
                    "Failure Line",
                    str(
                        failure_point.get(
                            "line",
                            "N/A"
                        )
                    )
                )

            st.markdown(
                """
                <div class="card">

                    <div class="card-title">
                        Error Message
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.code(
                log_result.get(
                    "error_message",
                    "Not Available"
                )
            )

            st.markdown(
                "#### 📍 Failure Point"
            )

            fp1, fp2, fp3, fp4 = st.columns(4)

            with fp1:

                st.write("**File**")

                st.code(
                    str(
                        failure_point.get(
                            "file",
                            "N/A"
                        )
                    )
                )

            with fp2:

                st.write("**Class**")

                st.code(
                    str(
                        failure_point.get(
                            "class",
                            "N/A"
                        )
                    )
                )

            with fp3:

                st.write("**Method**")

                st.code(
                    str(
                        failure_point.get(
                            "method",
                            "N/A"
                        )
                    )
                )

            with fp4:

                st.write("**Line**")

                st.code(
                    str(
                        failure_point.get(
                            "line",
                            "N/A"
                        )
                    )
                )

            code_path = log_result.get(
                "code_path",
                []
            )

            if code_path:

                st.markdown(
                    "#### 🔗 Code Path"
                )

                st.info(
                    " → ".join(
                        code_path
                    )
                )

        # =====================================================
        # TAB 3 - ROOT CAUSE
        # =====================================================

        with tab3:

            st.markdown(
                "### 🧠 Root Cause Analysis"
            )

            root_cause_text = root_cause.get(
                "root_cause",
                "Root cause analysis unavailable."
            )

            st.markdown(
                f"""
                <div class="root-card">

                    <div class="root-label">
                        Detected Root Cause
                    </div>

                    <div class="root-text">
                        {root_cause_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            rc1, rc2 = st.columns(2)

            with rc1:

                root_confidence = float(
                    root_cause.get(
                        "confidence",
                        0
                    )
                )

                st.metric(
                    "Analysis Confidence",
                    f"{root_confidence * 100:.0f}%"
                )

            with rc2:

                evidence_available = root_cause.get(
                    "evidence_available",
                    False
                )

                st.metric(
                    "Historical Evidence",
                    "Available"
                    if evidence_available
                    else "Limited"
                )

            with st.expander(
                "🔎 View Root Cause Reasoning"
            ):

                st.write(
                    root_cause.get(
                        "reasoning",
                        "No reasoning available."
                    )
                )

            supporting_evidence = root_cause.get(
                "supporting_evidence",
                []
            )

            if supporting_evidence:

                st.markdown(
                    "#### 📚 Supporting Historical Evidence"
                )

                evidence_rows = []

                for evidence in supporting_evidence:

                    evidence_rows.append(
                        {
                            "Bug ID": evidence.get(
                                "bug_id",
                                "Unknown"
                            ),

                            "Similarity": evidence.get(
                                "similarity_percentage",
                                "N/A"
                            ),

                            "Source": evidence.get(
                                "source",
                                "Unknown"
                            ),

                            "Historical Record": evidence.get(
                                "historical_text",
                                "Not Available"
                            )
                        }
                    )

                st.dataframe(
                    pd.DataFrame(
                        evidence_rows
                    ),
                    use_container_width=True,
                    hide_index=True
                )

        # =====================================================
        # TAB 4 - DUPLICATE DETECTION
        # =====================================================

        with tab4:

            st.markdown(
                "### 🔄 Duplicate Detection"
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

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Detection Status",
                    duplicate_status
                )

            with col2:

                st.metric(
                    "Matches Analyzed",
                    match_count
                )

            with col3:

                matching_bugs = duplicate_result.get(
                    "matching_bugs",
                    []
                )

                if matching_bugs:

                    top_similarity = matching_bugs[0].get(
                        "similarity_percentage",
                        0
                    )

                    try:

                        top_similarity = float(
                            top_similarity
                        )

                        top_similarity_text = (
                            f"{top_similarity:.2f}%"
                        )

                    except Exception:

                        top_similarity_text = str(
                            top_similarity
                        )

                else:

                    top_similarity_text = "N/A"

                st.metric(
                    "Top Match",
                    top_similarity_text
                )

            matching_bugs = duplicate_result.get(
                "matching_bugs",
                []
            )

            if matching_bugs:

                st.markdown(
                    "#### 📚 Historical Bug Matches"
                )

                match_rows = []

                for index, match in enumerate(
                    matching_bugs,
                    start=1
                ):

                    similarity = match.get(
                        "similarity_percentage",
                        0
                    )

                    try:

                        similarity = float(
                            similarity
                        )

                        similarity_text = (
                            f"{similarity:.2f}%"
                        )

                    except Exception:

                        similarity_text = str(
                            similarity
                        )

                    match_rows.append(
                        {
                            "Rank": index,

                            "Bug ID": match.get(
                                "bug_id",
                                "Unknown"
                            ),

                            "Similarity": similarity_text,

                            "Classification": match.get(
                                "status",
                                "Unknown"
                            ),

                            "Source": match.get(
                                "source",
                                "Unknown"
                            ),

                            "Historical Record": match.get(
                                "historical_text",
                                "Not Available"
                            )
                        }
                    )

                st.dataframe(
                    pd.DataFrame(
                        match_rows
                    ),
                    use_container_width=True,
                    hide_index=True
                )

                with st.expander(
                    "🔎 View Match Explanations"
                ):

                    for index, match in enumerate(
                        matching_bugs,
                        start=1
                    ):

                        st.markdown(
                            f"**Match {index} — "
                            f"{match.get('bug_id', 'Unknown')}**"
                        )

                        st.write(
                            match.get(
                                "explanation",
                                "No explanation available."
                            )
                        )

                        st.divider()

        # =====================================================
        # TAB 5 - REMEDIATION
        # =====================================================

        with tab5:

            st.markdown(
                "### 🛠️ Remediation Recommendation"
            )

            recommended_fix = remediation.get(
                "recommended_fix",
                "No recommendation available."
            )

            implementation_guidance = remediation.get(
                "implementation_guidance",
                "No implementation guidance available."
            )

            remediation_confidence = float(
                remediation.get(
                    "confidence",
                    0
                )
            )

            evidence_type = remediation.get(
                "evidence_type",
                "Unknown"
            )

            st.markdown(
                f"""
                <div class="fix-card">

                    <div class="fix-title">
                        🛠️ Recommended Fix
                    </div>

                    <div class="card-text">
                        {recommended_fix}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Recommendation Confidence",
                    f"{remediation_confidence * 100:.0f}%"
                )

            with col2:

                st.metric(
                    "Evidence Type",
                    evidence_type
                )

            st.markdown(
                "#### 🔧 Implementation Guidance"
            )

            st.info(
                implementation_guidance
            )

            historical_evidence = remediation.get(
                "historical_evidence",
                []
            )

            if historical_evidence:

                with st.expander(
                    "📚 Historical Fix References"
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

                        st.divider()

        # =====================================================
        # FINAL REPORT
        # =====================================================

        st.markdown(
            '<div class="section-title">📄 Final Diagnosis Report</div>',
            unsafe_allow_html=True
        )

        summary_data = {
            "Bug ID": bug_id,

            "Severity": triage.get(
                "severity",
                "Unknown"
            ),

            "Priority": triage.get(
                "priority",
                "Unknown"
            ),

            "Component": triage.get(
                "component",
                "Unknown"
            ),

            "Exception": log_result.get(
                "exception_type",
                "N/A"
            ),

            "Root Cause": root_cause.get(
                "root_cause",
                "N/A"
            ),

            "Duplicate Status": duplicate_status,

            "Recommended Fix": recommended_fix
        }

        st.dataframe(
            pd.DataFrame(
                [summary_data]
            ),
            use_container_width=True,
            hide_index=True
        )

        st.success(
            "✅ Complete structured bug diagnosis report generated successfully."
        )