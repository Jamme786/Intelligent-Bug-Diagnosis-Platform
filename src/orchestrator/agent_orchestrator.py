from agents.triage_agent import triage_bug
from agents.log_analysis_agent import analyze_logs
from agents.root_cause_agent import find_root_cause
from agents.duplicate_detection_agent import detect_duplicates
from agents.remediation_agent import recommend_fix


def diagnose_bug(bug):

    # -------------------------------------------------
    # Validate Bug Input
    # -------------------------------------------------

    if not bug or not isinstance(bug, dict):

        return {
            "Error": "Invalid bug input. Please provide a valid bug report."
        }

    # -------------------------------------------------
    # Step 1: Triage Agent
    # -------------------------------------------------

    try:

        triage_result = triage_bug(bug)

    except Exception as e:

        triage_result = {
            "severity": "Unknown",
            "priority": "Unknown",
            "component": "Unknown",
            "confidence": 0.0,
            "reasoning": "Triage Agent failed to analyze the bug."
        }

    # -------------------------------------------------
    # Step 2: Log Analysis Agent
    # -------------------------------------------------

    try:

        log_findings = analyze_logs(bug)

    except Exception as e:

        log_findings = {
            "exception_type": "Not Available",
            "error_message": "Log analysis failed.",
            "failure_point": {
                "file": "Not Available",
                "class": "Not Available",
                "method": "Not Available",
                "line": "Not Available"
            },
            "code_path": [],
            "confidence": 0.0
        }

    # -------------------------------------------------
    # Step 3: Root Cause Agent
    # -------------------------------------------------

    try:

        root_cause = find_root_cause(
            bug,
            log_findings
        )

    except Exception as e:

        root_cause = (
            "Root cause analysis could not be completed."
        )

    # -------------------------------------------------
    # Step 4: Duplicate Detection Agent
    # -------------------------------------------------

    try:

        duplicate_result = detect_duplicates(bug)

    except Exception as e:

        duplicate_result = {
            "duplicate_found": False,
            "similar_bugs": []
        }

    # -------------------------------------------------
    # Step 5: Fix Recommendation Agent
    # -------------------------------------------------

    try:

        recommendation = recommend_fix(
            bug,
            root_cause
        )

    except Exception as e:

        recommendation = (
            "Fix recommendation could not be generated."
        )

    # -------------------------------------------------
    # Combine All Agent Results
    # -------------------------------------------------

    result = {

        "Triage": triage_result,

        "Log Findings": log_findings,

        "Root Cause": root_cause,

        "Duplicate Detection": duplicate_result,

        "Recommended Fix": recommendation

    }

    return result