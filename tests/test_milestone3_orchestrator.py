import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


from orchestrator.agent_orchestrator import diagnose_bug


bug = {

    "Bug Title":
        "Critical Login Crash",

    "Bug Description":
        "Application crashes when fetching user during login.",

    "Stack Trace":
        "NullPointerException at UserService.java:45",

    "Error Log":
        "User object was null during login."
}


print("\n========================================")
print("MILESTONE 3 - COMPLETE ORCHESTRATOR TEST")
print("========================================")


result = diagnose_bug(bug)


print("\n--- TRIAGE ---")
print(result["Triage"])


print("\n--- LOG ANALYSIS ---")
print(result["Log Findings"])


print("\n--- ROOT CAUSE ---")
print(result["Root Cause"])


print("\n--- DUPLICATE DETECTION ---")
print(result["Duplicate Detection"])


print("\n--- REMEDIATION ---")
print(result["Recommended Fix"])


print("\n========================================")
print("MILESTONE 3 ORCHESTRATOR TEST COMPLETED")
print("========================================")