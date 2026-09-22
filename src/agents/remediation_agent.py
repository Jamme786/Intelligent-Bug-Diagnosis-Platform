def recommend_fix(
    bug,
    root_cause,
    duplicate_detection=None,
    triage=None,
    log_findings=None,
    historical_defects=None
):
    """
    Remediation Agent

    Generates an actionable fix using:
    1. Root Cause Agent output
    2. Duplicate Detection results
    3. Triage findings
    4. Log Analysis findings
    5. Historical defect evidence
    """

    if duplicate_detection is None:
        duplicate_detection = {}

    if triage is None:
        triage = {}

    if log_findings is None:
        log_findings = {}

    if historical_defects is None:
        historical_defects = []

    root_cause_text = str(root_cause).lower()

    bug_description = str(
        bug.get(
            "Bug Description",
            bug.get("Description", "")
        )
    )

    stack_trace = str(
        bug.get("Stack Trace", "")
    )

    error_log = str(
        bug.get("Error Log", "")
    )

    # ---------------------------------------------------------
    # Default values
    # ---------------------------------------------------------

    recommendation = (
        "Review the error logs, source code, and affected "
        "component to determine the appropriate fix."
    )

    implementation_guidance = (
        "Inspect the failure point, reproduce the issue, "
        "apply the fix, and validate the behavior with tests."
    )

    confidence = 0.50

    evidence_type = "Agent reasoning"

    historical_evidence = []

    # ---------------------------------------------------------
    # Collect historical evidence
    # ---------------------------------------------------------

    matching_bugs = duplicate_detection.get(
        "matching_bugs",
        []
    )

    for match in matching_bugs:

        if not isinstance(match, dict):
            continue

        similarity = float(
            match.get(
                "similarity_score",
                0.0
            )
        )

        if similarity >= 0.70:

            historical_evidence.append({
                "bug_id": match.get(
                    "bug_id",
                    "Unknown"
                ),

                "similarity": similarity,

                "historical_text": match.get(
                    "historical_text",
                    "Historical information unavailable."
                ),

                "source": match.get(
                    "source",
                    "Unknown"
                )
            })

    # ---------------------------------------------------------
    # Null pointer / null object issue
    # ---------------------------------------------------------

    if (
        "null object" in root_cause_text
        or "nullpointerexception" in root_cause_text
        or "null pointer" in root_cause_text
    ):

        recommendation = (
            "Add null validation before accessing the affected "
            "object. Initialize required objects properly and "
            "handle missing user or object data safely."
        )

        implementation_guidance = (
            "Inspect the failure point where the null object is "
            "accessed. Add a null check before the access, "
            "handle the missing value appropriately, and add "
            "a test case for the null-object scenario."
        )

        confidence = 0.88

        evidence_type = (
            "Root cause reasoning"
        )

    # ---------------------------------------------------------
    # Database issue
    # ---------------------------------------------------------

    elif (
        "database" in root_cause_text
        or "sql" in root_cause_text
    ):

        recommendation = (
            "Verify database connectivity, credentials, "
            "connection configuration, query execution, "
            "and database server availability."
        )

        implementation_guidance = (
            "Check the database configuration and connection "
            "settings. Validate the failing query and add "
            "appropriate database error handling. Test the "
            "connection and query after applying the fix."
        )

        confidence = 0.84

        evidence_type = (
            "Root cause reasoning"
        )

    # ---------------------------------------------------------
    # Timeout issue
    # ---------------------------------------------------------

    elif "timeout" in root_cause_text:

        recommendation = (
            "Identify the operation causing the timeout and "
            "optimize the operation or review the configured "
            "timeout value."
        )

        implementation_guidance = (
            "Inspect the slow operation, measure its execution "
            "time, optimize inefficient processing, and verify "
            "that the configured timeout is appropriate."
        )

        confidence = 0.82

        evidence_type = (
            "Root cause reasoning"
        )

    # ---------------------------------------------------------
    # Authentication issue
    # ---------------------------------------------------------

    elif (
        "authentication" in root_cause_text
        or "login" in root_cause_text
    ):

        recommendation = (
            "Review the authentication and login validation "
            "flow. Verify user credentials, authentication "
            "state, and handling of invalid or missing user data."
        )

        implementation_guidance = (
            "Inspect the authentication service and login "
            "validation logic. Add appropriate validation and "
            "error handling, then test valid and invalid "
            "authentication scenarios."
        )

        confidence = 0.80

        evidence_type = (
            "Root cause reasoning"
        )

    # ---------------------------------------------------------
    # Historical evidence available
    # ---------------------------------------------------------

    if historical_evidence:

        evidence_type = (
            "Historical evidence + agent reasoning"
        )

        # Increase confidence when a strong historical match
        # supports the recommendation.
        highest_similarity = max(
            item["similarity"]
            for item in historical_evidence
        )

        confidence = min(
            confidence + (
                highest_similarity * 0.05
            ),
            0.95
        )

    # ---------------------------------------------------------
    # Insufficient evidence
    # ---------------------------------------------------------

    if (
        root_cause_text.strip() == ""
        or
        "requires further analysis" in root_cause_text
    ):

        recommendation = (
            "Insufficient evidence to recommend a confirmed fix. "
            "Review the source code, logs, and failure conditions "
            "before applying a change."
        )

        implementation_guidance = (
            "Collect additional logs and reproduce the issue "
            "before implementing a fix."
        )

        confidence = 0.50

        evidence_type = (
            "Insufficient Evidence"
        )

    # ---------------------------------------------------------
    # Return structured result
    # ---------------------------------------------------------

    return {

        "recommended_fix": recommendation,

        "implementation_guidance":
            implementation_guidance,

        "confidence":
            round(confidence, 2),

        "evidence_type":
            evidence_type,

        "historical_evidence":
            historical_evidence,

        "bug_description":
            bug_description,

        "stack_trace":
            stack_trace,

        "error_log":
            error_log
    }