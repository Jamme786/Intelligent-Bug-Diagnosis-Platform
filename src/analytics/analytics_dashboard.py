import streamlit as st
import pandas as pd
import plotly.express as px

from .defect_pattern_analytics import DefectPatternAnalytics


# ---------------------------------------------------------
# SAMPLE ANALYTICS DATA
# ---------------------------------------------------------

BUG_DATA = [
    {
        "bug_id": "BUG-001",
        "severity": "Critical",
        "priority": "High",
        "component": "Authentication",
        "exception_type": "NullPointerException",
        "root_cause": "Missing null validation",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-002",
        "severity": "High",
        "priority": "High",
        "component": "Database",
        "exception_type": "SQLException",
        "root_cause": "Database connection failure",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-003",
        "severity": "Critical",
        "priority": "High",
        "component": "Authentication",
        "exception_type": "NullPointerException",
        "root_cause": "Missing null validation",
        "duplicate_status": "Likely Duplicate"
    },
    {
        "bug_id": "BUG-004",
        "severity": "Medium",
        "priority": "Medium",
        "component": "Payment",
        "exception_type": "TimeoutException",
        "root_cause": "External service timeout",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-005",
        "severity": "High",
        "priority": "High",
        "component": "Database",
        "exception_type": "SQLException",
        "root_cause": "Database connection failure",
        "duplicate_status": "Related"
    }
]


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

def defect_pattern_analytics_page():

    st.title("📊 Defect Pattern Analytics")

    st.markdown(
        """
        Analyze recurring defect patterns, affected components,
        severity, exceptions, root causes and duplicate trends.
        """
    )

    analytics = DefectPatternAnalytics(BUG_DATA)

    df = analytics.to_dataframe()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    st.sidebar.header("🔎 Analytics Filters")

    severity_options = ["All"] + sorted(df["severity"].unique().tolist())
    component_options = ["All"] + sorted(df["component"].unique().tolist())
    priority_options = ["All"] + sorted(df["priority"].unique().tolist())

    selected_severity = st.sidebar.selectbox(
        "Severity",
        severity_options
    )

    selected_component = st.sidebar.selectbox(
        "Component",
        component_options
    )

    selected_priority = st.sidebar.selectbox(
        "Priority",
        priority_options
    )

    filtered_df = df.copy()

    if selected_severity != "All":
        filtered_df = filtered_df[
            filtered_df["severity"] == selected_severity
        ]

    if selected_component != "All":
        filtered_df = filtered_df[
            filtered_df["component"] == selected_component
        ]

    if selected_priority != "All":
        filtered_df = filtered_df[
            filtered_df["priority"] == selected_priority
        ]

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    total_bugs = len(filtered_df)
    critical_bugs = len(
        filtered_df[filtered_df["severity"] == "Critical"]
    )
    affected_components = filtered_df["component"].nunique()

    duplicate_bugs = len(
        filtered_df[
            filtered_df["duplicate_status"] != "New"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Bugs",
        total_bugs
    )

    col2.metric(
        "Critical Bugs",
        critical_bugs
    )

    col3.metric(
        "Affected Components",
        affected_components
    )

    col4.metric(
        "Duplicate / Related",
        duplicate_bugs
    )

    st.divider()

    # -----------------------------------------------------
    # SEVERITY ANALYSIS
    # -----------------------------------------------------

    st.subheader("🚨 Severity Distribution")

    severity_df = (
        filtered_df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_df.columns = ["Severity", "Count"]

    fig_severity = px.bar(
        severity_df,
        x="Severity",
        y="Count",
        text="Count",
        title="Bug Severity Distribution"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )

    # -----------------------------------------------------
    # COMPONENT ANALYSIS
    # -----------------------------------------------------

    st.subheader("🧩 Affected Component Analysis")

    component_df = (
        filtered_df["component"]
        .value_counts()
        .reset_index()
    )

    component_df.columns = ["Component", "Count"]

    fig_component = px.pie(
        component_df,
        names="Component",
        values="Count",
        title="Bugs by Component"
    )

    st.plotly_chart(
        fig_component,
        use_container_width=True
    )

    # -----------------------------------------------------
    # EXCEPTION ANALYSIS
    # -----------------------------------------------------

    st.subheader("🐞 Recurring Exception Types")

    exception_df = (
        filtered_df["exception_type"]
        .value_counts()
        .reset_index()
    )

    exception_df.columns = ["Exception Type", "Count"]

    fig_exception = px.bar(
        exception_df,
        x="Exception Type",
        y="Count",
        text="Count",
        title="Recurring Exception Types"
    )

    st.plotly_chart(
        fig_exception,
        use_container_width=True
    )

    # -----------------------------------------------------
    # ROOT CAUSE ANALYSIS
    # -----------------------------------------------------

    st.subheader("🔍 Common Root Causes")

    root_df = (
        filtered_df["root_cause"]
        .value_counts()
        .reset_index()
    )

    root_df.columns = ["Root Cause", "Count"]

    st.dataframe(
        root_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # DUPLICATE ANALYSIS
    # -----------------------------------------------------

    st.subheader("♻️ Duplicate Detection Patterns")

    duplicate_df = (
        filtered_df["duplicate_status"]
        .value_counts()
        .reset_index()
    )

    duplicate_df.columns = ["Status", "Count"]

    fig_duplicate = px.pie(
        duplicate_df,
        names="Status",
        values="Count",
        title="Duplicate / Related Bug Status"
    )

    st.plotly_chart(
        fig_duplicate,
        use_container_width=True
    )

    # -----------------------------------------------------
    # BUG RECORDS
    # -----------------------------------------------------

    st.subheader("📋 Filtered Defect Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # INSIGHT SUMMARY
    # -----------------------------------------------------

    st.subheader("💡 Automated Pattern Insights")

    if not filtered_df.empty:

        most_affected = (
            filtered_df["component"]
            .value_counts()
            .idxmax()
        )

        common_exception = (
            filtered_df["exception_type"]
            .value_counts()
            .idxmax()
        )

        common_root_cause = (
            filtered_df["root_cause"]
            .value_counts()
            .idxmax()
        )

        st.info(
            f"""
            **Detected Patterns**

            • Most affected component: **{most_affected}**

            • Most recurring exception: **{common_exception}**

            • Most recurring root cause: **{common_root_cause}**

            • Total analyzed defects: **{len(filtered_df)}**
            """
        )

    else:

        st.warning(
            "No defect records match the selected filters."
        )