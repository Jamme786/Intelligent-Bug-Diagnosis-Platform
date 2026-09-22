from agents.triage_agent import triage_bug
from agents.log_analysis_agent import analyze_logs
from agents.root_cause_agent import find_root_cause
from agents.duplicate_detection_agent import detect_duplicates
from agents.remediation_agent import recommend_fix


def diagnose_bug(bug):

    # Validate input
    if not bug or not isinstance(bug, dict):
        return {
            "Error":
                "Invalid bug input. Please provide a valid bug report."
        }

    # ---------------------------------------------------------
    # 1. TRIAGE AGENT
    # ---------------------------------------------------------

    try:
        triage_result = triage_bug(bug)

    except Exception:
        triage_result = {
            "severity": "Unknown",
            "priority": "Unknown",
            "component": "Unknown",
            "confidence": 0.0,
            "reasoning":
                "Triage Agent failed to analyze the bug."
        }

    # ---------------------------------------------------------
    # 2. LOG ANALYSIS AGENT
    # ---------------------------------------------------------

    try:
        log_findings = analyze_logs(bug)

    except Exception:
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

    # ---------------------------------------------------------
    # 3. DUPLICATE DETECTION AGENT
    # ---------------------------------------------------------

    try:
        duplicate_result = detect_duplicates(bug)

    except Exception:
        duplicate_result = {
            "duplicate_status": "New/Unmatched",
            "duplicate_found": False,
            "match_count": 0,
            "matching_bugs": []
        }

    # ---------------------------------------------------------
    # 4. ROOT CAUSE AGENT
    # ---------------------------------------------------------

    try:

        historical_evidence = duplicate_result.get(
            "matching_bugs",
            []
        )

        root_cause = find_root_cause(
            bug,
            log_findings,
            historical_evidence
        )

    except Exception:
        root_cause = {
            "root_cause":
                "Root cause analysis could not be completed.",

            "confidence": 0.0,

            "failure_point":
                "Not Available",

            "reasoning":
                "Root Cause Agent failed to analyze the bug.",

            "supporting_evidence": [],

            "evidence_available": False
        }

    # ---------------------------------------------------------
    # 5. REMEDIATION AGENT
    # ---------------------------------------------------------

    try:

        # Extract root cause text
        root_cause_text = root_cause.get(
            "root_cause",
            ""
        )

        recommendation = recommend_fix(
            bug=bug,
            root_cause=root_cause_text,
            duplicate_detection=duplicate_result,
            triage=triage_result,
            log_findings=log_findings
        )

    except Exception:
        recommendation = {
            "recommended_fix":
                "Fix recommendation could not be generated.",

            "implementation_guidance":
                "Additional analysis is required.",

            "confidence": 0.0,

            "evidence_type":
                "Insufficient Evidence",

            "historical_evidence": []
        }

    # ---------------------------------------------------------
    # FINAL STRUCTURED RESULT
    # ---------------------------------------------------------

    result = {

        "Triage":
            triage_result,

        "Log Findings":
            log_findings,

        "Root Cause":
            root_cause,

        "Duplicate Detection":
            duplicate_result,

        "Recommended Fix":
            recommendation
    }

    return result