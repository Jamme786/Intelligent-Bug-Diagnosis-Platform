def triage_bug(bug):

    title = bug.get("Title", "")
    description = bug.get("Description", "")

    text = (title + " " + description).lower()

    if "crash" in text or "exception" in text:
        category = "Runtime Error"
        severity = "High"

    elif "login" in text or "authentication" in text:
        category = "Authentication Issue"
        severity = "Medium"

    elif "slow" in text or "performance" in text:
        category = "Performance Issue"
        severity = "Medium"

    else:
        category = "General Bug"
        severity = "Medium"

    return {
        "category": category,
        "severity": severity
    }