def find_root_cause(bug, log_findings):

    stack_trace = bug.get("Stack Trace", "").lower()
    error_log = bug.get("Error Log", "").lower()

    if "nullpointerexception" in stack_trace:
        cause = "A null object may be accessed during program execution."

    elif "database" in error_log:
        cause = "The issue may be related to database connectivity or query processing."

    elif "timeout" in error_log:
        cause = "The operation may be taking longer than the allowed timeout."

    else:
        cause = "Root cause requires further analysis."

    return cause