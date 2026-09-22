import sys
import os

# Add the project's src folder to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from agents.root_cause_agent import find_root_cause


# ============================================================
# TEST 1 - Critical Login Crash
# ============================================================

bug1 = {
    "Bug Title": "Critical Login Crash",
    "Bug Description": "Application crashes when fetching user during login.",
    "Stack Trace": "NullPointerException at UserService.java:45",
    "Error Log": "User object was null"
}

log_findings1 = {
    "exception_type": "NullPointerException",
    "error_message": "User object was null",
    "failure_point": "UserService.java:45"
}

historical_defects1 = [
    {
        "bug_id": "BUG-101",
        "description": "Login crashes because user object is null",
        "component": "Authentication",
        "exception": "NullPointerException",
        "resolution": "Added null validation before accessing user object"
    },
    {
        "bug_id": "BUG-102",
        "description": "User authentication failed because user object was empty",
        "component": "Authentication",
        "exception": "NullPointerException",
        "resolution": "Added validation for missing user object"
    }
]


print("\n========================================")
print("MILESTONE 3 - ROOT CAUSE TEST")
print("========================================")

result1 = find_root_cause(
    bug1,
    log_findings1,
    historical_defects1
)

print("\n--- ROOT CAUSE RESULT ---")
print("Root Cause:", result1["root_cause"])
print("Confidence:", result1["confidence"])
print("Failure Point:", result1["failure_point"])
print("Reasoning:", result1["reasoning"])
print("Evidence Available:", result1["evidence_available"])

print("\n--- SUPPORTING HISTORICAL EVIDENCE ---")

if result1["supporting_evidence"]:
    for defect in result1["supporting_evidence"]:
        print("\nBug ID:", defect.get("bug_id", "Unknown"))
        print("Description:", defect.get("description", "Not available"))
        print("Component:", defect.get("component", "Not available"))
        print("Exception:", defect.get("exception", "Not available"))
        print("Resolution:", defect.get("resolution", "Not available"))
else:
    print("No supporting historical evidence found.")


# ============================================================
# TEST 2 - Database Connection Failure
# ============================================================

bug2 = {
    "Bug Title": "Database Connection Failure",
    "Bug Description": "Application cannot connect to the database.",
    "Stack Trace": "",
    "Error Log": "SQLException: Connection refused"
}

log_findings2 = {
    "exception_type": "SQLException",
    "error_message": "Connection refused",
    "failure_point": "DatabaseService.java:78"
}

historical_defects2 = [
    {
        "bug_id": "BUG-201",
        "description": "Database connection refused by server",
        "component": "Database",
        "exception": "SQLException",
        "resolution": "Checked database server configuration and connection settings"
    }
]


print("\n========================================")
print("DATABASE ROOT CAUSE TEST")
print("========================================")

result2 = find_root_cause(
    bug2,
    log_findings2,
    historical_defects2
)

print("\n--- ROOT CAUSE RESULT ---")
print("Root Cause:", result2["root_cause"])
print("Confidence:", result2["confidence"])
print("Failure Point:", result2["failure_point"])
print("Reasoning:", result2["reasoning"])
print("Evidence Available:", result2["evidence_available"])

print("\n--- SUPPORTING HISTORICAL EVIDENCE ---")

if result2["supporting_evidence"]:
    for defect in result2["supporting_evidence"]:
        print("\nBug ID:", defect.get("bug_id", "Unknown"))
        print("Description:", defect.get("description", "Not available"))
        print("Component:", defect.get("component", "Not available"))
        print("Exception:", defect.get("exception", "Not available"))
        print("Resolution:", defect.get("resolution", "Not available"))
else:
    print("No supporting historical evidence found.")


# ============================================================
# TEST 3 - Unknown Bug
# ============================================================

bug3 = {
    "Bug Title": "Unknown Application Issue",
    "Bug Description": "Some unexpected behavior occurred.",
    "Stack Trace": "",
    "Error Log": ""
}

log_findings3 = {
    "exception_type": "",
    "error_message": "",
    "failure_point": ""
}

result3 = find_root_cause(
    bug3,
    log_findings3,
    []
)

print("\n========================================")
print("UNKNOWN BUG ROOT CAUSE TEST")
print("========================================")

print("Root Cause:", result3["root_cause"])
print("Confidence:", result3["confidence"])
print("Failure Point:", result3["failure_point"])
print("Reasoning:", result3["reasoning"])
print("Evidence Available:", result3["evidence_available"])


print("\n========================================")
print("ROOT CAUSE TESTS COMPLETED")
print("========================================")