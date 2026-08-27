def recommend_fix(bug, root_cause):

    if "null object" in root_cause.lower():

        recommendation = (
            "Check for null values before accessing objects. "
            "Initialize required objects and add appropriate null checks."
        )

    elif "database" in root_cause.lower():

        recommendation = (
            "Check database connection settings, credentials, "
            "queries, and database availability."
        )

    elif "timeout" in root_cause.lower():

        recommendation = (
            "Check the slow operation and optimize the process "
            "or review the configured timeout."
        )

    else:

        recommendation = (
            "Review the error logs and source code to determine "
            "the appropriate fix."
        )

    return recommendation