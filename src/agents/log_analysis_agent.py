import re


def analyze_logs(bug):

    stack_trace = bug.get("Stack Trace", "")
    error_log = bug.get("Error Log", "")

    # Combine available logs
    logs = stack_trace + "\n" + error_log

    # Default values
    exception_type = "Not Available"
    error_message = "Not Available"
    file_name = "Not Available"
    class_name = "Not Available"
    method_name = "Not Available"
    line_number = "Not Available"
    code_path = []
    confidence = 0.50

    # =================================================
    # 1. IDENTIFY EXCEPTION TYPE
    # =================================================

    exception_pattern = r"\b([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))\b"

    match = re.search(exception_pattern, logs)

    if match:
        exception_type = match.group(1)
        confidence += 0.10

    # =================================================
    # 2. EXTRACT ERROR MESSAGE
    # =================================================

    if exception_type != "Not Available":

        lines = logs.splitlines()

        for line in lines:

            line = line.strip()

            if exception_type not in line:
                continue

            # -------------------------------------------------
            # Case 1:
            # NullPointerException: user object is null
            # -------------------------------------------------

            if ":" in line:

                # Check whether this is a Java file reference
                # such as UserService.java:45
                java_reference = re.search(
                    r"\b[\w.-]+\.java:\d+\b",
                    line
                )

                if java_reference and line.startswith(exception_type):

                    # Example:
                    # NullPointerException at UserService.java:45
                    if re.search(
                        r"\bat\s+[\w.-]+\.java:\d+\b",
                        line
                    ):
                        pass

                    else:
                        message = line.split(":", 1)[1].strip()

                        if message:
                            error_message = message

            # -------------------------------------------------
            # Case 2:
            # NullPointerException at UserService.java:45
            # -------------------------------------------------

            elif re.search(
                r"\bat\s+[\w.-]+\.java:\d+\b",
                line
            ):

                # This is only a failure-point reference.
                # Do NOT use 45 as the error message.
                pass

            # -------------------------------------------------
            # Case 3:
            # NullPointerException user object is null
            # -------------------------------------------------

            else:

                cleaned_message = re.sub(
                    r"^" + re.escape(exception_type),
                    "",
                    line
                ).strip()

                if cleaned_message:
                    error_message = cleaned_message

            confidence += 0.10
            break

    # =================================================
    # 3. HANDLE PLAIN ERROR LOGS
    # =================================================

    if error_message == "Not Available" and error_log.strip():

        for line in error_log.splitlines():

            line = line.strip()

            if not line:
                continue

            if (
                "ERROR" in line.upper()
                or "FAIL" in line.upper()
                or "FAILED" in line.upper()
            ):

                if "-" in line:
                    error_message = line.split("-", 1)[1].strip()
                else:
                    error_message = line

                confidence += 0.05
                break

        # If there is no ERROR/FAIL keyword,
        # use the first meaningful error-log line.
        if error_message == "Not Available":

            error_message = error_log.strip().splitlines()[0].strip()
            confidence += 0.05

    # =================================================
    # 4. EXTRACT JAVA FAILURE POINT
    # =================================================

    # Supports:
    # at UserService.java:45
    # at com.example.UserService.login(UserService.java:45)

    java_pattern = (
        r"(?:at\s+)?"
        r"(?:(?P<class_path>[\w.$]+)\.)?"
        r"(?P<method>[\w$]+)"
        r"\("
        r"(?P<file>[\w.-]+\.java):"
        r"(?P<line>\d+)"
        r"\)"
    )

    java_matches = re.findall(
        java_pattern,
        logs
    )

    # Also support:
    # NullPointerException at UserService.java:45
    short_java_pattern = (
        r"(?P<file>[\w.-]+\.java):(?P<line>\d+)"
    )

    short_java_matches = re.findall(
        short_java_pattern,
        logs
    )

    if java_matches:

        first_match = java_matches[0]

        full_class = first_match[0]
        method_name = first_match[1]
        file_name = first_match[2]
        line_number = first_match[3]

        if full_class:

            class_name = full_class.split(".")[-1]

        else:

            class_name = file_name.replace(
                ".java",
                ""
            )

        confidence += 0.10

        # Create code path
        for match in java_matches:

            full_class = match[0]
            method = match[1]

            if full_class:

                class_name_path = full_class.split(".")[-1]

            else:

                class_name_path = match[2].replace(
                    ".java",
                    ""
                )

            code_path.append(
                class_name_path + "." + method
            )

    elif short_java_matches:

        first_match = short_java_matches[0]

        file_name = first_match[0]
        line_number = first_match[1]

        class_name = file_name.replace(
            ".java",
            ""
        )

        method_name = "Not Available"

        confidence += 0.10

        code_path.append(
            class_name
        )

    # =================================================
    # 5. PYTHON STACK TRACE SUPPORT
    # =================================================

    python_pattern = (
        r'File\s+"([^"]+)",\s+line\s+(\d+)'
    )

    python_matches = re.findall(
        python_pattern,
        logs
    )

    if (
        python_matches
        and file_name == "Not Available"
    ):

        file_name = python_matches[0][0]
        line_number = python_matches[0][1]

        confidence += 0.10

        for match in python_matches:

            code_path.append(
                match[0] + ":" + match[1]
            )

    # =================================================
    # 6. DETECT AVAILABLE LOGS
    # =================================================

    if stack_trace:
        confidence += 0.05

    if error_log:
        confidence += 0.05

    # Maximum confidence = 0.95
    confidence = min(
        confidence,
        0.95
    )

    # =================================================
    # 7. STRUCTURED RESULT
    # =================================================

    result = {

        "exception_type":
            exception_type,

        "error_message":
            error_message,

        "failure_point": {

            "file":
                file_name,

            "class":
                class_name,

            "method":
                method_name,

            "line":
                line_number
        },

        "code_path":
            code_path,

        "confidence":
            round(
                confidence,
                2
            )
    }

    return result