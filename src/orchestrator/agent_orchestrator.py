from agents.triage_agent import triage_bug
from agents.log_analysis_agent import analyze_logs
from agents.root_cause_agent import find_root_cause
from agents.duplicate_detection_agent import detect_duplicates
from agents.remediation_agent import recommend_fix


def diagnose_bug(bug):

    # Step 1: Triage
    triage_result = triage_bug(bug)

    # Step 2: Log Analysis
    log_findings = analyze_logs(bug)

    # Step 3: Root Cause
    root_cause = find_root_cause(
        bug,
        log_findings
    )

    # Step 4: Duplicate Detection
    duplicate_result = detect_duplicates(bug)

    # Step 5: Fix Recommendation
    recommendation = recommend_fix(
        bug,
        root_cause
    )

    result = {
        "Triage": triage_result,
        "Log Findings": log_findings,
        "Root Cause": root_cause,
        "Duplicate Detection": duplicate_result,
        "Recommended Fix": recommendation
    }

    return result