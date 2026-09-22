from knowledge_base.vector_store import search_similar_bugs


def detect_duplicates(bug):
    """
    Duplicate Detection Agent

    Searches the historical defect knowledge base
    and identifies potentially duplicate or related bugs.
    """

    title = bug.get(
        "Title",
        bug.get("Bug Title", "")
    )

    description = bug.get(
        "Description",
        bug.get("Bug Description", "")
    )

    stack_trace = bug.get(
        "Stack Trace",
        ""
    )

    error_log = bug.get(
        "Error Log",
        ""
    )

    # Create semantic search query
    query = (
        str(title) + " " +
        str(description) + " " +
        str(stack_trace) + " " +
        str(error_log)
    ).strip()

    # Search historical bugs
    similar_bugs = search_similar_bugs(
        query,
        top_k=5
    )

    matches = []

    for bug_result in similar_bugs:

        similarity = float(
            bug_result.get(
                "similarity",
                0.0
            )
        )

        bug_id = bug_result.get(
            "bug_id",
            "Unknown"
        )

        text = bug_result.get(
            "text",
            "Historical defect information unavailable."
        )

        source = bug_result.get(
            "source",
            "Unknown"
        )

        distance = bug_result.get(
            "distance",
            0.0
        )

        # Classification thresholds
        if similarity >= 0.85:

            status = "Likely Duplicate"

            explanation = (
                "High semantic similarity was found "
                "between the submitted bug and this "
                "historical defect."
            )

        elif similarity >= 0.70:

            status = "Related Issue"

            explanation = (
                "The historical defect has meaningful "
                "similarity with the submitted bug, "
                "but it may represent a related issue "
                "rather than an exact duplicate."
            )

        else:

            status = "New/Unmatched"

            explanation = (
                "The similarity score is low, so this "
                "historical defect is unlikely to be "
                "a duplicate."
            )

        matches.append({

            "bug_id": bug_id,

            "similarity_score": round(
                similarity,
                4
            ),

            "similarity_percentage": round(
                similarity * 100,
                2
            ),

            "distance": round(
                float(distance),
                4
            ),

            "status": status,

            "historical_text": text,

            "source": source,

            "resolution": (
                "Historical resolution information "
                "is not available in the current "
                "knowledge-base record."
            ),

            "explanation": explanation
        })

    # Rank highest similarity first
    matches.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    # Overall status
    if not matches:

        overall_status = "New/Unmatched"

    elif matches[0]["similarity_score"] >= 0.85:

        overall_status = "Likely Duplicate"

    elif matches[0]["similarity_score"] >= 0.70:

        overall_status = "Related Issue"

    else:

        overall_status = "New/Unmatched"

    return {

        "duplicate_status": overall_status,

        "duplicate_found": (
            overall_status == "Likely Duplicate"
        ),

        "match_count": len(matches),

        "matching_bugs": matches
    }