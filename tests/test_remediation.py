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


from agents.remediation_agent import recommend_fix


print("\n========================================")
print("MILESTONE 3 - REMEDIATION AGENT TEST")
print("========================================")


# ============================================================
# TEST 1 - NULL POINTER ISSUE
# ============================================================

bug = {
    "Bug Description":
        "Application crashes during login.",

    "Stack Trace":
        "NullPointerException at UserService.java:45",

    "Error Log":
        "User object was null."
}


root_cause = (
    "A null object is likely being accessed "
    "without proper null validation."
)


duplicate_detection = {
    "matching_bugs": [
        {
            "bug_id": "BUG-101",
            "similarity_score": 0.91,
            "historical_text":
                "Login crashes because user object is null",
            "source": "Historical Dataset"
        }
    ]
}


result = recommend_fix(
    bug,
    root_cause,
    duplicate_detection
)


print("\n--- NULL POINTER REMEDIATION ---")

print(
    "Recommended Fix:",
    result["recommended_fix"]
)

print(
    "Implementation Guidance:",
    result["implementation_guidance"]
)

print(
    "Confidence:",
    result["confidence"]
)

print(
    "Evidence Type:",
    result["evidence_type"]
)

print(
    "Historical Evidence:",
    result["historical_evidence"]
)


# ============================================================
# TEST 2 - DATABASE ISSUE
# ============================================================

bug = {
    "Bug Description":
        "Application cannot connect to database.",

    "Stack Trace":
        "SQLException at DatabaseService.java:78",

    "Error Log":
        "Connection refused."
}


root_cause = (
    "The issue may be related to database "
    "connectivity or query processing."
)


result = recommend_fix(
    bug,
    root_cause
)


print("\n--- DATABASE REMEDIATION ---")

print(
    "Recommended Fix:",
    result["recommended_fix"]
)

print(
    "Implementation Guidance:",
    result["implementation_guidance"]
)

print(
    "Confidence:",
    result["confidence"]
)

print(
    "Evidence Type:",
    result["evidence_type"]
)


# ============================================================
# TEST 3 - INSUFFICIENT EVIDENCE
# ============================================================

bug = {
    "Bug Description":
        "Application behaves unexpectedly.",

    "Stack Trace":
        "",

    "Error Log":
        ""
}


root_cause = (
    "Root cause requires further analysis."
)


result = recommend_fix(
    bug,
    root_cause
)


print("\n--- INSUFFICIENT EVIDENCE TEST ---")

print(
    "Recommended Fix:",
    result["recommended_fix"]
)

print(
    "Implementation Guidance:",
    result["implementation_guidance"]
)

print(
    "Confidence:",
    result["confidence"]
)

print(
    "Evidence Type:",
    result["evidence_type"]
)


print("\n========================================")
print("REMEDIATION TESTS COMPLETED")
print("========================================")