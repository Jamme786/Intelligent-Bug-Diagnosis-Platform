def find_root_cause(bug, log_findings, historical_defects=None):
    """
    Root Cause Agent

    Determines a probable root cause using:
    1. Bug information
    2. Log Analysis findings
    3. Historical defect information
    """

    if historical_defects is None:
        historical_defects = []

    # Get information from the bug
    description = bug.get("Bug Description", "").lower()
    stack_trace = bug.get("Stack Trace", "").lower()
    error_log = bug.get("Error Log", "").lower()

    # Get information from Log Analysis Agent
    exception_type = str(
        log_findings.get("exception_type", "")
    ).lower()

    error_message = str(
        log_findings.get("error_message", "")
    ).lower()

    failure_point = str(
        log_findings.get("failure_point", "")
    )

    # Combine available information
    combined_text = " ".join([
        description,
        stack_trace,
        error_log,
        exception_type,
        error_message
    ])

    # Default values
    cause = "Root cause requires further analysis."
    confidence = 0.50
    reasoning = "Insufficient evidence was available."

    # Root cause rules
    if "nullpointerexception" in combined_text or "null pointer" in combined_text:
        cause = "A null object is likely being accessed without proper null validation."
        confidence = 0.87
        reasoning = (
            "The submitted bug contains NullPointerException information. "
            "This commonly indicates that an object is being accessed before "
            "checking whether it contains a valid value."
        )

    elif "database" in combined_text or "sql" in combined_text:
        cause = "The issue may be related to database connectivity or query processing."
        confidence = 0.82
        reasoning = (
            "The bug and log information contain database-related errors. "
            "This indicates a possible connectivity, query, or database "
            "configuration problem."
        )

    elif "timeout" in combined_text:
        cause = "The operation may be exceeding the configured timeout limit."
        confidence = 0.80
        reasoning = (
            "Timeout information was found in the submitted bug or logs. "
            "This suggests that the operation is taking longer than the "
            "allowed execution time."
        )

    elif "authentication" in combined_text or "login" in combined_text:
        cause = "The authentication or login flow may contain a validation or configuration issue."
        confidence = 0.78
        reasoning = (
            "The submitted bug contains authentication or login-related "
            "information, indicating a possible issue in the authentication flow."
        )

    # Historical evidence
    supporting_evidence = []

    for defect in historical_defects:
        if not isinstance(defect, dict):
            continue

        defect_text = " ".join(
            str(value).lower()
            for value in defect.values()
        )

        # Check whether the historical defect is related
        if (
            ("nullpointerexception" in combined_text and
             "nullpointerexception" in defect_text)
            or
            ("database" in combined_text and
             "database" in defect_text)
            or
            ("timeout" in combined_text and
             "timeout" in defect_text)
            or
            ("authentication" in combined_text and
             "authentication" in defect_text)
        ):
            supporting_evidence.append(defect)

    # Increase confidence when historical evidence exists
    if supporting_evidence:
        confidence = min(confidence + 0.05, 0.95)

    return {
        "root_cause": cause,
        "confidence": round(confidence, 2),
        "failure_point": failure_point,
        "reasoning": reasoning,
        "supporting_evidence": supporting_evidence,
        "evidence_available": bool(supporting_evidence)
    }