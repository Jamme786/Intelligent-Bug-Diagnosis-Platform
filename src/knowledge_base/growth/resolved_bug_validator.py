class ResolvedBugValidator:

    REQUIRED_FIELDS = [
        "bug_id",
        "component",
        "severity",
        "root_cause",
        "resolution",
        "status"
    ]

    def validate(self, bug):
        """
        Validate whether a resolved bug contains
        enough information to be added to the
        Knowledge Base.
        """

        if not isinstance(bug, dict):
            return False, "Bug record must be a dictionary."

        # Check required fields
        for field in self.REQUIRED_FIELDS:

            if field not in bug:
                return False, f"Missing required field: {field}"

            if bug[field] is None:
                return False, f"Empty value for field: {field}"

            if str(bug[field]).strip() == "":
                return False, f"Empty value for field: {field}"

        # Only resolved bugs can be added
        if str(bug["status"]).lower() != "resolved":
            return False, "Bug is not marked as resolved."

        return True, "Bug is valid for Knowledge Base growth."


if __name__ == "__main__":

    validator = ResolvedBugValidator()

    test_bug = {
        "bug_id": "BUG-006",
        "component": "Authentication",
        "severity": "High",
        "root_cause": "Missing null validation",
        "resolution": "Added null validation before accessing user session.",
        "status": "Resolved"
    }

    valid, message = validator.validate(test_bug)

    print("Validation Result:", valid)
    print("Message:", message)