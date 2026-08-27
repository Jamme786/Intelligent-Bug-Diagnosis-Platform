from src.orchestrator.agent_orchestrator import diagnose_bug


bug = {
    "Title": "Application crashes during login",

    "Description": "The application crashes when the user tries to log in.",

    "Stack Trace": "NullPointerException at LoginService.login()",

    "Error Log": "ERROR: Login service failed"
}


result = diagnose_bug(bug)


print("\n===== BUG DIAGNOSIS =====")

print("\nTriage:")
print(result["Triage"])

print("\nLog Analysis:")
print(result["Log Findings"])

print("\nRoot Cause:")
print(result["Root Cause"])

print("\nDuplicate Detection:")
print(result["Duplicate Detection"])

print("\nRecommended Fix:")
print(result["Recommended Fix"])