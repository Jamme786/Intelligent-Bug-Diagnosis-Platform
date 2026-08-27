# Intelligent Bug Diagnosis Platform

## 1. System Overview

The Intelligent Bug Diagnosis Platform is an AI-based system that analyzes software bug reports, error logs, and stack traces.

The system uses historical defect data, semantic search, RAG, and AI agents to identify similar bugs, determine possible root causes, and recommend fixes.

---

## 2. System Architecture

```text
                    USER
                      |
                      v
            +-------------------+
            | Streamlit Web UI  |
            +-------------------+
                      |
                      v
            +-------------------+
            | Bug Submission    |
            | Module            |
            +-------------------+
                      |
                      v
            +-------------------+
            | Bug Processing    |
            | Module            |
            +-------------------+
                      |
                      v
            +-------------------+
            | Agent Orchestrator|
            +-------------------+
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
     Triage Agent  Log Agent  Root Cause
          |           |           |
          +-----------+-----------+
                      |
                      v
          +-----------------------+
          | Duplicate Detection   |
          | Agent                 |
          +-----------------------+
                      |
                      v
          +-----------------------+
          | RAG Retrieval Pipeline|
          +-----------------------+
                      |
                      v
          +-----------------------+
          | Vector Database       |
          | FAISS                 |
          +-----------------------+
                      |
                      v
          +-----------------------+
          | Historical Bug Data   |
          | Mozilla / Apache /    |
          | Eclipse               |
          +-----------------------+
                      |
                      v
          +-----------------------+
          | Remediation Agent     |
          +-----------------------+
                      |
                      v
          +-----------------------+
          | Diagnosis & Fix       |
          | Recommendation       |
          +-----------------------+
                      |
                      v
                    USER