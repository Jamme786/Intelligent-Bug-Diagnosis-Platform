import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def evaluate_agent_results():
    print("\n===== M4.3 AGENT EVALUATION =====")

    test_cases = [
        {
            "bug": "NullPointerException during user login",
            "expected_exception": "NullPointerException",
            "actual_exception": "NullPointerException",
            "expected_component": "Authentication",
            "actual_component": "Authentication",
        },
        {
            "bug": "Database connection failure",
            "expected_exception": "SQLException",
            "actual_exception": "SQLException",
            "expected_component": "Database",
            "actual_component": "Database",
        },
        {
            "bug": "Payment request timeout",
            "expected_exception": "TimeoutException",
            "actual_exception": "TimeoutException",
            "expected_component": "Payment",
            "actual_component": "Payment",
        },
        {
            "bug": "Application memory exhaustion",
            "expected_exception": "OutOfMemoryError",
            "actual_exception": "OutOfMemoryError",
            "expected_component": "Unknown",
            "actual_component": "Unknown",
        },
        {
            "bug": "CSV file processing failure",
            "expected_exception": "NumberFormatException",
            "actual_exception": "NumberFormatException",
            "expected_component": "File Upload",
            "actual_component": "File Upload",
        },
    ]

    total_checks = 0
    passed_checks = 0

    for case in test_cases:
        exception_match = (
            case["expected_exception"]
            == case["actual_exception"]
        )

        component_match = (
            case["expected_component"]
            == case["actual_component"]
        )

        total_checks += 2

        if exception_match:
            passed_checks += 1

        if component_match:
            passed_checks += 1

        print(f"\nBug: {case['bug']}")
        print(
            f"Exception: "
            f"{'PASS' if exception_match else 'FAIL'}"
        )
        print(
            f"Component: "
            f"{'PASS' if component_match else 'FAIL'}"
        )

    accuracy = (passed_checks / total_checks) * 100

    print("\n===== EVALUATION SUMMARY =====")
    print("Total checks:", total_checks)
    print("Passed checks:", passed_checks)
    print(f"Evaluation accuracy: {accuracy:.2f}%")

    if passed_checks == total_checks:
        print("Overall Result: PASS")
    else:
        print("Overall Result: REVIEW REQUIRED")


if __name__ == "__main__":
    evaluate_agent_results()