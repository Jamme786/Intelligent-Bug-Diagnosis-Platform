from knowledge_base.vector_store import search_similar_bugs


def detect_duplicates(bug):

    title = bug.get("Title", "")
    description = bug.get("Description", "")
    stack_trace = bug.get("Stack Trace", "")

    query = (
        title + " " +
        description + " " +
        stack_trace
    )

    similar_bugs = search_similar_bugs(
        query,
        top_k=3
    )

    if len(similar_bugs) > 0:

        return {
            "duplicate_found": True,
            "similar_bugs": similar_bugs
        }

    return {
        "duplicate_found": False,
        "similar_bugs": []
    }