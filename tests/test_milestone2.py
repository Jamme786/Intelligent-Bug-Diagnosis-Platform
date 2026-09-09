import sys
import os

# -------------------------------------------------
# Add src folder to Python path
# -------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from agents.triage_agent import triage_bug
from agents.log_analysis_agent import analyze_logs


# =================================================
# TEST 1: Critical Login Crash
# =================================================

bug1 = {
    "Title": "Login Crash",
    "Description": "Application crashes when the user logs in.",
    "Stack Trace": """java.lang.NullPointerException: User object was null
    at com.example.UserService.getUser(UserService.java:45)
    at com.example.UserController.fetchUser(UserController.java:20)""",
    "Error Log": ""
}


# =================================================
# TEST 2: High Severity Database Error
# =================================================

bug2 = {
    "Title": "Database Error",
    "Description": "Database connection failure prevents users from accessing data.",
    "Stack Trace": """java.sql.SQLException: Connection refused
    at com.example.DatabaseService.connect(DatabaseService.java:78)""",
    "Error Log": ""
}


# =================================================
# TEST 3: Medium UI Bug
# =================================================

bug3 = {
    "Title": "Button Not Working",
    "Description": "The submit button is not working when the user tries to save the form.",
    "Stack Trace": "",
    "Error Log": ""
}


# =================================================
# TEST 4: File Upload Error
# =================================================

bug4 = {
    "Title": "File Upload Failure",
    "Description": "File upload failure occurs when uploading a document.",
    "Stack Trace": "",
    "Error Log": "ERROR FileUploadService - Upload failed"
}


# =================================================
# TEST 5: Python Error
# =================================================

bug5 = {
    "Title": "Python Application Error",
    "Description": "Application shows an error while processing user data.",
    "Stack Trace": """Traceback (most recent call last):
  File "app.py", line 25, in process_data
    result = data["name"]
KeyError: 'name'""",
    "Error Log": ""
}


# =================================================
# FUNCTION TO TEST A BUG
# =================================================

def test_bug(bug, test_name):

    print("\n========================================")
    print(test_name)
    print("========================================")

    # -------------------------------------------------
    # Triage Agent
    # -------------------------------------------------

    print("\n--- TRIAGE RESULT ---")

    try:

        triage_result = triage_bug(bug)

        print(
            "Severity:",
            triage_result["severity"]
        )

        print(
            "Priority:",
            triage_result["priority"]
        )

        print(
            "Component:",
            triage_result["component"]
        )

        print(
            "Confidence:",
            triage_result["confidence"]
        )

        print(
            "Reasoning:",
            triage_result["reasoning"]
        )

    except Exception as e:

        print(
            "Triage Agent Error:",
            e
        )

    # -------------------------------------------------
    # Log Analysis Agent
    # -------------------------------------------------

    print("\n--- LOG ANALYSIS RESULT ---")

    try:

        log_result = analyze_logs(bug)

        print(
            "Exception:",
            log_result["exception_type"]
        )

        print(
            "Error Message:",
            log_result["error_message"]
        )

        failure_point = log_result["failure_point"]

        print(
            "File:",
            failure_point["file"]
        )

        print(
            "Class:",
            failure_point["class"]
        )

        print(
            "Method:",
            failure_point["method"]
        )

        print(
            "Line:",
            failure_point["line"]
        )

        print(
            "Code Path:",
            log_result["code_path"]
        )

        print(
            "Confidence:",
            log_result["confidence"]
        )

    except Exception as e:

        print(
            "Log Analysis Agent Error:",
            e
        )


# =================================================
# RUN ALL TESTS
# =================================================

test_bug(
    bug1,
    "TEST 1 - Critical Login Crash"
)

test_bug(
    bug2,
    "TEST 2 - Database Connection Failure"
)

test_bug(
    bug3,
    "TEST 3 - Medium UI Bug"
)

test_bug(
    bug4,
    "TEST 4 - File Upload Error"
)

test_bug(
    bug5,
    "TEST 5 - Python Error"
)


print("\n========================================")
print("ALL MILESTONE 2 TESTS COMPLETED")
print("========================================")