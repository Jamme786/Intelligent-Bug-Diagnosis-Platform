import streamlit as st

from bug_submission.bug_submission_backup import bug_submission_page
from analytics.analytics_dashboard import defect_pattern_analytics_page


st.set_page_config(
    page_title="Intelligent Bug Diagnosis Platform",
    page_icon="🐞",
    layout="wide"
)


st.sidebar.title("🐞 Bug Diagnosis Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Bug Submission",
        "Defect Pattern Analytics"
    ]
)


if page == "Bug Submission":
    bug_submission_page()

elif page == "Defect Pattern Analytics":
    defect_pattern_analytics_page()