import os
from datetime import datetime

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from .resolved_bug_validator import ResolvedBugValidator


MODEL_NAME = "all-MiniLM-L6-v2"

INDEX_FILE = "data/processed/vector_store/bug_index.faiss"
METADATA_FILE = "data/processed/vector_store/bug_metadata.pkl"


class KnowledgeBaseGrowth:

    def __init__(self):
        self.validator = ResolvedBugValidator()
        self.model = SentenceTransformer(MODEL_NAME)

    def create_bug_text(self, bug):
        """
        Create a consistent text representation
        of a resolved bug for embedding.
        """

        return (
            f"Bug ID: {bug['bug_id']}. "
            f"Component: {bug['component']}. "
            f"Severity: {bug['severity']}. "
            f"Root Cause: {bug['root_cause']}. "
            f"Resolution: {bug['resolution']}."
        )

    def add_resolved_bug(self, bug):

        # =================================================
        # 1. VALIDATE BUG
        # =================================================

        valid, message = self.validator.validate(bug)

        if not valid:
            return {
                "success": False,
                "message": message
            }

        # =================================================
        # 2. CHECK VECTOR STORE FILES
        # =================================================

        if not os.path.exists(INDEX_FILE):
            return {
                "success": False,
                "message": "FAISS vector store not found."
            }

        if not os.path.exists(METADATA_FILE):
            return {
                "success": False,
                "message": "Knowledge Base metadata not found."
            }

        # =================================================
        # 3. LOAD EXISTING VECTOR STORE
        # =================================================

        try:
            index = faiss.read_index(INDEX_FILE)
            metadata = pd.read_pickle(METADATA_FILE)

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to load Knowledge Base: "
                    f"{error}"
                )
            }

        # =================================================
        # 4. PREVENT DUPLICATE BUG IDs
        # =================================================

        if "bug_id" in metadata.columns:

            existing_ids = (
                metadata["bug_id"]
                .astype(str)
                .tolist()
            )

            if str(bug["bug_id"]) in existing_ids:

                return {
                    "success": False,
                    "message": (
                        f"Bug {bug['bug_id']} "
                        "already exists in the Knowledge Base."
                    )
                }

        # =================================================
        # 5. CREATE BUG TEXT
        # =================================================

        bug_text = self.create_bug_text(bug)

        # =================================================
        # 6. GENERATE EMBEDDING
        # =================================================

        try:

            embedding = self.model.encode(
                [bug_text]
            )

            embedding = np.array(
                embedding
            ).astype("float32")

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to generate bug embedding: "
                    f"{error}"
                )
            }

        # =================================================
        # 7. NORMALIZE EMBEDDING
        # =================================================

        faiss.normalize_L2(
            embedding
        )

        # =================================================
        # 8. ADD EMBEDDING TO FAISS
        # =================================================

        try:

            index.add(
                embedding
            )

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to add embedding to "
                    f"FAISS vector store: {error}"
                )
            }

        # =================================================
        # 9. CREATE METADATA RECORD
        # =================================================

        new_record = {

            "bug_id":
                bug["bug_id"],

            "component":
                bug["component"],

            "severity":
                bug["severity"],

            "root_cause":
                bug["root_cause"],

            "resolution":
                bug["resolution"],

            "status":
                bug["status"],

            "source":
                "resolved_bug",

            "timestamp":
                datetime.now().isoformat(),

            "text":
                bug_text,

            "chunk_type":
                "resolved_bug"
        }

        # =================================================
        # 10. ADD METADATA
        # =================================================

        new_metadata = pd.DataFrame(
            [new_record]
        )

        updated_metadata = pd.concat(
            [
                metadata,
                new_metadata
            ],
            ignore_index=True
        )

        # =================================================
        # 11. SAVE UPDATED FAISS INDEX
        # =================================================

        try:

            faiss.write_index(
                index,
                INDEX_FILE
            )

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to save FAISS vector store: "
                    f"{error}"
                )
            }

        # =================================================
        # 12. SAVE UPDATED METADATA
        # =================================================

        try:

            updated_metadata.to_pickle(
                METADATA_FILE
            )

        except Exception as error:

            return {
                "success": False,
                "message": (
                    "Failed to save Knowledge Base metadata: "
                    f"{error}"
                )
            }

        # =================================================
        # 13. SUCCESS RESPONSE
        # =================================================

        return {

            "success":
                True,

            "message":
                (
                    f"Bug {bug['bug_id']} "
                    "successfully added to the "
                    "Knowledge Base."
                ),

            "total_vectors":
                index.ntotal
        }


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    growth = KnowledgeBaseGrowth()

    resolved_bug = {

        "bug_id":
            "BUG-006",

        "component":
            "Authentication",

        "severity":
            "High",

        "root_cause":
            "Missing null validation",

        "resolution":
            (
                "Added null validation before "
                "accessing the user session."
            ),

        "status":
            "Resolved"
    }

    result = growth.add_resolved_bug(
        resolved_bug
    )

    print(
        "\n===== KNOWLEDGE BASE GROWTH ====="
    )

    print(
        "Success:",
        result["success"]
    )

    print(
        "Message:",
        result["message"]
    )

    if result["success"]:

        print(
            "Total vectors:",
            result["total_vectors"]
        )