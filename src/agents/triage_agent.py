import re


class TriageAgent:

    def analyze(self, bug_description):

        # Make sure the description is always a string
        if not isinstance(bug_description, str):
            bug_description = ""

        description = bug_description.lower()

        # -------------------------------------------------
        # Severity and Priority
        # -------------------------------------------------

        if (
            "crash" in description
            or "system down" in description
        ):
            severity = "Critical"
            priority = "High"

        elif (
            "error" in description
            or "failure" in description
            or "failed" in description
        ):
            severity = "High"
            priority = "High"

        elif (
            "incorrect" in description
            or "not working" in description
        ):
            severity = "Medium"
            priority = "Medium"

        else:
            severity = "Low"
            priority = "Low"

        # -------------------------------------------------
        # Affected Component
        # -------------------------------------------------

        if (
            "login" in description
            or "log in" in description
            or "logs in" in description
            or "logged in" in description
            or "authentication" in description
            or "authenticate" in description
        ):
            component = "Authentication"

        elif (
            "database" in description
            or "database connection" in description
        ):
            component = "Database"

        elif (
            "payment" in description
            or "transaction" in description
        ):
            component = "Payment"

        elif (
            "upload" in description
            or "file upload" in description
        ):
            component = "File Upload"

        elif (
            re.search(r"\bui\b", description)
            or re.search(r"\bbutton\b", description)
            or re.search(r"\bscreen\b", description)
            or re.search(r"\bweb page\b", description)
            or re.search(r"\buser interface\b", description)
            or re.search(r"\bform\b", description)
        ):
            component = "UI"

        else:
            component = "Unknown"

        # -------------------------------------------------
        # Structured Result
        # -------------------------------------------------

        return {
            "severity": severity,
            "priority": priority,
            "component": component,
            "confidence": 0.85,
            "reasoning": "Classification based on keywords and bug impact."
        }


def triage_bug(bug):

    agent = TriageAgent()

    # Safely get Description
    if not isinstance(bug, dict):
        description = ""
    else:
        description = bug.get(
            "Description",
            ""
        )

    return agent.analyze(
        description
    )