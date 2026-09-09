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
# VALIDATION DATASET
# =================================================

test_cases = [

    # -------------------------------------------------
    # TEST 1 - Normal Java Crash
    # -------------------------------------------------

    {
        "name": "Login Crash",

        "bug": {
            "Title": "Login Crash",
            "Description": "Application crashes when the user logs in.",
            "Stack Trace": """java.lang.NullPointerException: User object was null
    at com.example.UserService.getUser(UserService.java:45)
    at com.example.UserController.fetchUser(UserController.java:20)""",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "Critical",
            "priority": "High",
            "component": "Authentication"
        },

        "expected_log": {
            "exception_type": "NullPointerException",
            "file": "UserService.java",
            "line": "45"
        }
    },


    # -------------------------------------------------
    # TEST 2 - Database Failure
    # -------------------------------------------------

    {
        "name": "Database Failure",

        "bug": {
            "Title": "Database Error",
            "Description": "Database connection failure prevents users from accessing data.",
            "Stack Trace": """java.sql.SQLException: Connection refused
    at com.example.DatabaseService.connect(DatabaseService.java:78)""",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Database"
        },

        "expected_log": {
            "exception_type": "SQLException",
            "file": "DatabaseService.java",
            "line": "78"
        }
    },


    # -------------------------------------------------
    # TEST 3 - Description Only
    # -------------------------------------------------

    {
        "name": "Description Only",

        "bug": {
            "Title": "Payment Error",
            "Description": "Payment transaction failed while processing the customer order.",
            "Stack Trace": "",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Payment"
        },

        "expected_log": {
            "exception_type": "Not Available",
            "file": "Not Available",
            "line": "Not Available"
        }
    },


    # -------------------------------------------------
    # TEST 4 - Logs Only
    # -------------------------------------------------

    {
        "name": "Logs Only",

        "bug": {
            "Title": "",
            "Description": "",
            "Stack Trace": "",
            "Error Log": "ERROR FileUploadService - Upload failed"
        },

        "expected_triage": {
            "severity": "Low",
            "priority": "Low",
            "component": "Unknown"
        },

        "expected_log": {
            "exception_type": "Not Available",
            "file": "Not Available",
            "line": "Not Available"
        }
    },


    # -------------------------------------------------
    # TEST 5 - Python Error
    # -------------------------------------------------

    {
        "name": "Python Error",

        "bug": {
            "Title": "Python Application Error",
            "Description": "Application shows an error while processing user data.",
            "Stack Trace": """Traceback (most recent call last):
  File "app.py", line 25, in process_data
    result = data["name"]
KeyError: 'name'""",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Unknown"
        },

        "expected_log": {
            "exception_type": "KeyError",
            "file": "app.py",
            "line": "25"
        }
    },


    # -------------------------------------------------
    # TEST 6 - Messy Java Log
    # -------------------------------------------------

    {
        "name": "Messy Java Log",

        "bug": {
            "Title": "Service Error",
            "Description": "The application shows an error while loading user information.",
            "Stack Trace": """2026-09-08 10:30:22 ERROR
java.lang.IllegalArgumentException: Invalid user ID
at com.example.UserService.loadUser(UserService.java:91)
at com.example.UserController.getUser(UserController.java:32)
random log text here""",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Unknown"
        },

        "expected_log": {
            "exception_type": "IllegalArgumentException",
            "file": "UserService.java",
            "line": "91"
        }
    },


    # -------------------------------------------------
    # TEST 7 - Authentication Stack Trace
    # -------------------------------------------------

    {
        "name": "Authentication Failure",

        "bug": {
            "Title": "Authentication Failure",
            "Description": "Authentication error occurs when the user tries to log in.",
            "Stack Trace": """java.lang.SecurityException: Access denied
    at com.example.AuthService.authenticate(AuthService.java:55)""",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Authentication"
        },

        "expected_log": {
            "exception_type": "SecurityException",
            "file": "AuthService.java",
            "line": "55"
        }
    },


    # -------------------------------------------------
    # TEST 8 - No Logs
    # -------------------------------------------------

    {
        "name": "Missing Logs",

        "bug": {
            "Title": "Form Issue",
            "Description": "The form is not working correctly.",
            "Stack Trace": "",
            "Error Log": ""
        },

        "expected_triage": {
            "severity": "Medium",
            "priority": "Medium",
            "component": "UI"
        },

        "expected_log": {
            "exception_type": "Not Available",
            "file": "Not Available",
            "line": "Not Available"
        }
    },


    # -------------------------------------------------
    # TEST 9 - File Upload
    # -------------------------------------------------

    {
        "name": "File Upload",

        "bug": {
            "Title": "Upload Problem",
            "Description": "File upload failure occurs when uploading a document.",
            "Stack Trace": "",
            "Error Log": "ERROR FileUploadService - Upload failed"
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "File Upload"
        },

        "expected_log": {
            "exception_type": "Not Available",
            "file": "Not Available",
            "line": "Not Available"
        }
    },


    # -------------------------------------------------
    # TEST 10 - Database Log
    # -------------------------------------------------

    {
        "name": "Database Log",

        "bug": {
            "Title": "Database Connection Problem",
            "Description": "Database connection failure occurs when loading customer data.",
            "Stack Trace": "",
            "Error Log": "ERROR DatabaseService - Connection timeout"
        },

        "expected_triage": {
            "severity": "High",
            "priority": "High",
            "component": "Database"
        },

        "expected_log": {
            "exception_type": "Not Available",
            "file": "Not Available",
            "line": "Not Available"
        }
    }
]


# =================================================
# ACCURACY COUNTERS
# =================================================

severity_correct = 0
priority_correct = 0
component_correct = 0

exception_correct = 0
failure_point_correct = 0

total = len(test_cases)


# =================================================
# FAILURE RECORD
# =================================================

failures = []


# =================================================
# RUN VALIDATION
# =================================================

for case in test_cases:

    print("\n========================================")
    print(case["name"])
    print("========================================")

    bug = case["bug"]

    # -------------------------------------------------
    # Triage Validation
    # -------------------------------------------------

    triage = triage_bug(bug)

    print("\nTriage Result:")
    print(triage)

    if triage["severity"] == case["expected_triage"]["severity"]:
        severity_correct += 1
    else:
        failures.append(
            case["name"] + " - Severity"
        )

    if triage["priority"] == case["expected_triage"]["priority"]:
        priority_correct += 1
    else:
        failures.append(
            case["name"] + " - Priority"
        )

    if triage["component"] == case["expected_triage"]["component"]:
        component_correct += 1
    else:
        failures.append(
            case["name"] + " - Component"
        )

    # -------------------------------------------------
    # Log Analysis Validation
    # -------------------------------------------------

    log_result = analyze_logs(bug)

    print("\nLog Analysis Result:")
    print(log_result)

    if (
        log_result["exception_type"]
        == case["expected_log"]["exception_type"]
    ):
        exception_correct += 1
    else:
        failures.append(
            case["name"] + " - Exception Type"
        )

    failure_point = log_result["failure_point"]

    if (
        failure_point["file"]
        == case["expected_log"]["file"]
        and
        failure_point["line"]
        == case["expected_log"]["line"]
    ):
        failure_point_correct += 1
    else:
        failures.append(
            case["name"] + " - Failure Point"
        )


# =================================================
# CALCULATE ACCURACY
# =================================================

severity_accuracy = (
    severity_correct / total
) * 100

priority_accuracy = (
    priority_correct / total
) * 100

component_accuracy = (
    component_correct / total
) * 100

exception_accuracy = (
    exception_correct / total
) * 100

failure_point_accuracy = (
    failure_point_correct / total
) * 100


# =================================================
# FINAL REPORT
# =================================================

print("\n\n========================================")
print("MILESTONE 2.4 ACCURACY REPORT")
print("========================================")

print(
    f"Severity Accuracy: "
    f"{severity_accuracy:.2f}%"
)

print(
    f"Priority Accuracy: "
    f"{priority_accuracy:.2f}%"
)

print(
    f"Component Accuracy: "
    f"{component_accuracy:.2f}%"
)

print(
    f"Exception Accuracy: "
    f"{exception_accuracy:.2f}%"
)

print(
    f"Failure Point Accuracy: "
    f"{failure_point_accuracy:.2f}%"
)

print("\nTotal Test Cases:", total)


# =================================================
# FAILURE ANALYSIS
# =================================================

print("\n========================================")
print("FAILURE ANALYSIS")
print("========================================")

if len(failures) == 0:

    print("No incorrect predictions found.")

else:

    print(
        "Incorrect predictions:"
    )

    for failure in failures:

        print(
            "-",
            failure
        )


print("\n========================================")
print("VALIDATION COMPLETED")
print("========================================")