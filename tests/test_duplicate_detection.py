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


from agents.duplicate_detection_agent import detect_duplicates


print("\n========================================")
print("MILESTONE 3 - DUPLICATE DETECTION TEST")
print("========================================")


# ============================================================
# TEST 1 - KNOWN DUPLICATE
# ============================================================

duplicate_bug = {

    "Title": "Login NullPointerException",

    "Description": (
        "Application crashes when user logs in "
        "because the user object is null."
    ),

    "Stack Trace": (
        "NullPointerException at LoginService.login()"
    ),

    "Error Log": (
        "User object was null during login."
    )
}


print("\n\n========================================")
print("TEST 1 - KNOWN DUPLICATE")
print("========================================")


result = detect_duplicates(
    duplicate_bug
)


print(
    "\nDuplicate Status:",
    result["duplicate_status"]
)

print(
    "Duplicate Found:",
    result["duplicate_found"]
)

print(
    "Match Count:",
    result["match_count"]
)


for match in result["matching_bugs"]:

    print("\n------------------------------")

    print(
        "Bug ID:",
        match["bug_id"]
    )

    print(
        "Similarity:",
        str(match["similarity_percentage"]) + "%"
    )

    print(
        "Status:",
        match["status"]
    )

    print(
        "Historical Text:",
        match["historical_text"]
    )

    print(
        "Source:",
        match["source"]
    )

    print(
        "Explanation:",
        match["explanation"]
    )


# ============================================================
# TEST 2 - RELATED ISSUE
# ============================================================

related_bug = {

    "Title": "Authentication Error",

    "Description": (
        "Login fails during authentication and "
        "shows an unexpected error."
    ),

    "Stack Trace": (
        "AuthenticationException at "
        "AuthService.authenticate()"
    ),

    "Error Log": (
        "Authentication failed."
    )
}


print("\n\n========================================")
print("TEST 2 - RELATED ISSUE")
print("========================================")


result = detect_duplicates(
    related_bug
)


print(
    "\nDuplicate Status:",
    result["duplicate_status"]
)

print(
    "Duplicate Found:",
    result["duplicate_found"]
)

print(
    "Match Count:",
    result["match_count"]
)


for match in result["matching_bugs"][:3]:

    print("\n------------------------------")

    print(
        "Bug ID:",
        match["bug_id"]
    )

    print(
        "Similarity:",
        str(match["similarity_percentage"]) + "%"
    )

    print(
        "Status:",
        match["status"]
    )

    print(
        "Historical Text:",
        match["historical_text"]
    )

    print(
        "Source:",
        match["source"]
    )

    print(
        "Explanation:",
        match["explanation"]
    )


# ============================================================
# TEST 3 - UNRELATED BUG
# ============================================================

unrelated_bug = {

    "Title": "UI Button Color Issue",

    "Description": (
        "The submit button is displayed with "
        "the wrong background color."
    ),

    "Stack Trace": "",

    "Error Log": (
        "CSS styling issue in the submit button."
    )
}


print("\n\n========================================")
print("TEST 3 - UNRELATED BUG")
print("========================================")


result = detect_duplicates(
    unrelated_bug
)


print(
    "\nDuplicate Status:",
    result["duplicate_status"]
)

print(
    "Duplicate Found:",
    result["duplicate_found"]
)

print(
    "Match Count:",
    result["match_count"]
)


for match in result["matching_bugs"][:3]:

    print("\n------------------------------")

    print(
        "Bug ID:",
        match["bug_id"]
    )

    print(
        "Similarity:",
        str(match["similarity_percentage"]) + "%"
    )

    print(
        "Status:",
        match["status"]
    )

    print(
        "Historical Text:",
        match["historical_text"]
    )

    print(
        "Source:",
        match["source"]
    )

    print(
        "Explanation:",
        match["explanation"]
    )


print("\n========================================")
print("DUPLICATE DETECTION TESTS COMPLETED")
print("========================================")