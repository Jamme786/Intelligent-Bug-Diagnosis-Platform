def analyze_logs(bug):

    stack_trace = bug.get("Stack Trace", "")
    error_log = bug.get("Error Log", "")

    findings = []

    if stack_trace:
        findings.append("Stack trace detected.")

    if error_log:
        findings.append("Error log detected.")

    if "nullpointerexception" in stack_trace.lower():
        findings.append("NullPointerException detected.")

    if "error" in error_log.lower():
        findings.append("Error message detected in logs.")

    return findings