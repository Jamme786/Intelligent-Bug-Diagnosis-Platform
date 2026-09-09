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

    # -------------------------------------------------
    # 1. Identify Exception Type
    # -------------------------------------------------

    exception_patterns = [
        r'\b([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))\b'
    ]

    for pattern in exception_patterns:

        match = re.search(
            pattern,
            logs
        )

        if match:

            exception_type = match.group(1)

            confidence += 0.10

            break

    # -------------------------------------------------
    # 2. Extract Error Message
    # -------------------------------------------------

    if exception_type != "Not Available":

        lines = logs.splitlines()

        for line in lines:

            if exception_type in line:

                message = line.strip()

                if ":" in message:

                    error_message = message.split(
                        ":",
                        1
                    )[1].strip()

                else:

                    error_message = message

                confidence += 0.10

                break

    # -------------------------------------------------
    # 3. Handle Plain Error Logs
    # -------------------------------------------------

    if error_message == "Not Available" and error_log:

        for line in error_log.splitlines():

            line = line.strip()

            if (
                "ERROR" in line.upper()
                or "FAIL" in line.upper()
                or "FAILED" in line.upper()
            ):

                if "-" in line:

                    error_message = line.split(
                        "-",
                        1
                    )[1].strip()

                else:

                    error_message = line

                confidence += 0.05

                break

    # -------------------------------------------------
    # 4. Extract Java Failure Point
    # -------------------------------------------------

    java_pattern = (
        r'at\s+([\w.]+)\.([\w$]+)'
        r'\(([\w.-]+):(\d+)\)'
    )

    java_matches = re.findall(
        java_pattern,
        logs
    )

    if java_matches:

        first_match = java_matches[0]

        full_class = first_match[0]

        method_name = first_match[1]

        file_name = first_match[2]

        line_number = first_match[3]

        class_name = full_class.split(
            "."
        )[-1]

        confidence += 0.10

        # Create code path

        for match in java_matches:

            full_class = match[0]

            method = match[1]

            class_name_path = full_class.split(
                "."
            )[-1]

            code_path.append(
                class_name_path + "." + method
            )

    # -------------------------------------------------
    # 5. Python Stack Trace Support
    # -------------------------------------------------

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

    # -------------------------------------------------
    # 6. Detect Available Logs
    # -------------------------------------------------

    if stack_trace:

        confidence += 0.05

    if error_log:

        confidence += 0.05

    # Maximum confidence = 0.95

    confidence = min(
        confidence,
        0.95
    )

    # -------------------------------------------------
    # 7. Structured Result
    # -------------------------------------------------

    result = {

        "exception_type": exception_type,

        "error_message": error_message,

        "failure_point": {

            "file": file_name,

            "class": class_name,

            "method": method_name,

            "line": line_number
        },

        "code_path": code_path,

        "confidence": round(
            confidence,
            2
        )
    }

    return result