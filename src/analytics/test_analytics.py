from defect_pattern_analytics import DefectPatternAnalytics


bugs = [
    {
        "bug_id": "BUG-001",
        "severity": "Critical",
        "priority": "High",
        "component": "Authentication",
        "exception_type": "NullPointerException",
        "root_cause": "Missing null validation",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-002",
        "severity": "High",
        "priority": "High",
        "component": "Database",
        "exception_type": "SQLException",
        "root_cause": "Database connection failure",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-003",
        "severity": "Critical",
        "priority": "High",
        "component": "Authentication",
        "exception_type": "NullPointerException",
        "root_cause": "Missing null validation",
        "duplicate_status": "Likely Duplicate"
    },
    {
        "bug_id": "BUG-004",
        "severity": "Medium",
        "priority": "Medium",
        "component": "Payment",
        "exception_type": "TimeoutException",
        "root_cause": "External service timeout",
        "duplicate_status": "New"
    },
    {
        "bug_id": "BUG-005",
        "severity": "High",
        "priority": "High",
        "component": "Database",
        "exception_type": "SQLException",
        "root_cause": "Database connection failure",
        "duplicate_status": "Related"
    }
]


analytics = DefectPatternAnalytics(bugs)

print("\n===== DEFECT PATTERN ANALYTICS =====")

print("\nTotal Bugs:")
print(analytics.get_summary()["total_bugs"])

print("\nSeverity Distribution:")
print(analytics.severity_distribution())

print("\nPriority Distribution:")
print(analytics.priority_distribution())

print("\nComponent Distribution:")
print(analytics.component_distribution())

print("\nException Distribution:")
print(analytics.exception_distribution())

print("\nRoot Cause Distribution:")
print(analytics.root_cause_distribution())

print("\nDuplicate Distribution:")
print(analytics.duplicate_distribution())