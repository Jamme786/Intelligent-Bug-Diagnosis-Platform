from src.agents.triage_agent import triage_bug
from src.agents.log_analysis_agent import analyze_logs
from src.agents.root_cause_agent import find_root_cause


def test_triage_bug():

    bug = {
        "Title": "Application crash",
        "Description": "Application throws an exception."
    }

    result = triage_bug(bug)

    assert result["category"] == "Runtime Error"


def test_log_analysis():

    bug = {
        "Stack Trace": "NullPointerException",
        "Error Log": "ERROR: Application failed"
    }

    result = analyze_logs(bug)

    assert len(result) > 0


def test_root_cause():

    bug = {
        "Stack Trace": "NullPointerException",
        "Error Log": ""
    }

    findings = ["NullPointerException detected."]

    result = find_root_cause(bug, findings)

    assert "null object" in result.lower()