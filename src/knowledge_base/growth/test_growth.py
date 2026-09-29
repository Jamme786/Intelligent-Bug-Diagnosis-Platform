import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from src.knowledge_base.growth.resolved_bug_validator import (
    ResolvedBugValidator
)

from src.knowledge_base.growth.knowledge_base_growth import (
    KnowledgeBaseGrowth
)

from src.knowledge_base.vector_store import (
    search_similar_bugs
)


def print_result(test_name, passed, details=""):
    print("\n" + "=" * 60)
    print(test_name)
    print("=" * 60)

    if passed:
        print("PASS")
    else:
        print("FAIL")

    if details:
        print(details)


# =========================================================
# TEST 1 - VALID RESOLVED BUG
# =========================================================

def test_valid_resolved_bug():

    validator = ResolvedBugValidator()

    bug = {
        "bug_id": "TEST-001",
        "component": "Authentication",
        "severity": "High",
        "root_cause": "Missing null validation",
        "resolution": (
            "Added null validation before "
            "accessing the user session."
        ),
        "status": "Resolved"
    }

    valid, message = validator.validate(bug)

    print_result(
        "TEST 1 - Valid Resolved Bug",
        valid,
        f"Validation Result: {valid}\n"
        f"Message: {message}"
    )

    return valid


# =========================================================
# TEST 2 - UNRESOLVED BUG
# =========================================================

def test_unresolved_bug():

    validator = ResolvedBugValidator()

    bug = {
        "bug_id": "TEST-002",
        "component": "Database",
        "severity": "High",
        "root_cause": "Database connection failure",
        "resolution": "Database configuration updated.",
        "status": "Open"
    }

    valid, message = validator.validate(bug)

    passed = not valid

    print_result(
        "TEST 2 - Unresolved Bug Rejection",
        passed,
        f"Validation Result: {valid}\n"
        f"Message: {message}"
    )

    return passed


# =========================================================
# TEST 3 - INCOMPLETE BUG
# =========================================================

def test_incomplete_bug():

    validator = ResolvedBugValidator()

    bug = {
        "bug_id": "TEST-003",
        "component": "Payment",
        "severity": "Medium",
        "root_cause": "Payment timeout",
        "status": "Resolved"
    }

    valid, message = validator.validate(bug)

    passed = not valid

    print_result(
        "TEST 3 - Incomplete Bug Rejection",
        passed,
        f"Validation Result: {valid}\n"
        f"Message: {message}"
    )

    return passed


# =========================================================
# TEST 4 - INVALID OBJECT
# =========================================================

def test_invalid_object():

    validator = ResolvedBugValidator()

    bug = "This is not a bug dictionary"

    valid, message = validator.validate(bug)

    passed = not valid

    print_result(
        "TEST 4 - Invalid Record Rejection",
        passed,
        f"Validation Result: {valid}\n"
        f"Message: {message}"
    )

    return passed


# =========================================================
# TEST 5 - KNOWLEDGE BASE GROWTH
# =========================================================

def test_knowledge_base_growth():

    print("\n" + "=" * 60)
    print("TEST 5 - Knowledge Base Growth")
    print("=" * 60)

    growth = KnowledgeBaseGrowth()

    bug = {
        "bug_id": "TEST-GROWTH-002",
        "component": "Authentication",
        "severity": "High",
        "root_cause": "Missing null validation",
        "resolution": (
            "Added null validation before "
            "accessing the user session."
        ),
        "status": "Resolved",
        "source": "Submitted Bug",
        "timestamp": "2026-09-28"
    }

    try:

        result = growth.add_resolved_bug(bug)

        print("Growth Result:")
        print(result)

        return result.get("success", False)

    except Exception as error:

        print("Growth test failed.")
        print("Error:", error)

        return False


# =========================================================
# TEST 6 - DUPLICATE PREVENTION
# =========================================================

def test_duplicate_prevention():

    print("\n" + "=" * 60)
    print("TEST 6 - Duplicate Prevention")
    print("=" * 60)

    growth = KnowledgeBaseGrowth()

    bug = {
        "bug_id": "TEST-GROWTH-001",
        "component": "Authentication",
        "severity": "High",
        "root_cause": "Missing null validation",
        "resolution": (
            "Added null validation before "
            "accessing the user session."
        ),
        "status": "Resolved",
        "source": "Submitted Bug",
        "timestamp": "2026-09-28"
    }

    try:

        result = growth.add_resolved_bug(bug)

        print("Second insertion result:")
        print(result)

        passed = (
            result.get("success") is False
            and "already exists" in result.get(
                "message", ""
            )
        )

        if passed:
            print("Duplicate correctly rejected.")

        return passed

    except Exception as error:

        print("Duplicate prevention test failed.")
        print("Error:", error)

        return False


# =========================================================
# TEST 7 - SEMANTIC RETRIEVAL
# =========================================================

def test_semantic_retrieval():

    print("\n" + "=" * 60)
    print("TEST 7 - Semantic Retrieval")
    print("=" * 60)

    query = (
        "User session is null and causes "
        "authentication login crash"
    )

    print("Search Query:")
    print(query)

    try:

        results = search_similar_bugs(
            query,
            top_k=5
        )

        if not results:

            print("\nNo similar bugs were retrieved.")

            return False

        print("\nRetrieved Results:")

        for index, result in enumerate(
            results,
            start=1
        ):

            print(f"\nResult {index}")

            print(
                "Bug ID:",
                result.get("bug_id")
            )

            print(
                "Similarity:",
                result.get("similarity")
            )

            print(
                "Source:",
                result.get("source")
            )

            print(
                "Text:",
                result.get("text")
            )

        print(
            "\nSemantic retrieval successful."
        )

        return True

    except Exception as error:

        print(
            "\nSemantic retrieval test failed."
        )

        print(
            "Error:",
            error
        )

        return False


# =========================================================
# MAIN TEST SUITE
# =========================================================

def main():

    print("\n")
    print("=" * 60)
    print(" M4.2 KNOWLEDGE BASE GROWTH TEST SUITE")
    print("=" * 60)

    results = []

    results.append(
        test_valid_resolved_bug()
    )

    results.append(
        test_unresolved_bug()
    )

    results.append(
        test_incomplete_bug()
    )

    results.append(
        test_invalid_object()
    )

    results.append(
        test_knowledge_base_growth()
    )

    results.append(
        test_duplicate_prevention()
    )

    results.append(
        test_semantic_retrieval()
    )

    passed = sum(results)
    total = len(results)

    print("\n")
    print("=" * 60)
    print(" FINAL TEST SUMMARY")
    print("=" * 60)

    print(
        f"Tests Passed: {passed}/{total}"
    )

    if passed == total:

        print(
            "STATUS: ALL TESTS PASSED"
        )

    else:

        print(
            "STATUS: SOME TESTS NEED ATTENTION"
        )

    print("=" * 60)


if __name__ == "__main__":

    main()