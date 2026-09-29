# Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance

## M4.4 Technical Documentation

### 1. Project Overview

The Intelligent Bug Diagnosis Platform is an AI-assisted software debugging system designed to analyze submitted software bugs and provide structured diagnosis and fix recommendations.

The platform processes bug descriptions, stack traces, and error logs through multiple specialized agents. It combines rule-based analysis, historical defect retrieval, semantic similarity, and knowledge-base information to support automated bug diagnosis.

### 2. Project Objectives

The main objectives of the platform are:

* Automate initial bug classification and diagnosis.
* Identify bug severity, priority, and affected component.
* Extract exception types and failure points from logs and stack traces.
* Identify possible root causes.
* Detect similar or related historical defects.
* Recommend possible fixes using historical evidence and agent reasoning.
* Continuously grow the Knowledge Base using resolved bugs.
* Provide defect pattern analytics and visual insights.
* Evaluate the complete diagnosis pipeline using different bug types and input formats.

---

## 3. System Architecture

The platform follows a modular multi-agent architecture.

### Main Components

1. Bug Submission Module
2. Triage Agent
3. Log Analysis Agent
4. Root Cause Agent
5. Duplicate Detection Agent
6. Remediation Agent
7. Knowledge Base
8. RAG Retrieval System
9. Knowledge Base Growth Mechanism
10. Defect Pattern Analytics Module
11. Streamlit User Interface
12. Orchestration Layer

### Architecture Flow

```text
                    User
                     |
                     v
             Bug Submission
                     |
                     v
              Orchestrator
                     |
        +------------+------------+
        |            |            |
        v            v            v
     Triage      Log Analysis   Root Cause
        |            |            |
        +------------+------------+
                     |
                     v
             Duplicate Detection
                     |
                     v
               Remediation
                     |
                     v
              Diagnosis Report
                     |
          +----------+----------+
          |                     |
          v                     v
     Knowledge Base       Defect Analytics
          |
          v
     RAG Retrieval
```

---

## 4. Bug Submission Module

The Bug Submission Module provides the main input interface.

Users can submit:

* Bug title
* Bug description
* Stack trace
* Error log
* TXT files
* LOG files
* CSV files

The application supports files up to 200 MB per file.

Each submitted bug receives a unique Bug ID.

Example:

```text
BUG-20260929091655
```

The submitted information is passed to the diagnosis pipeline for processing.

---

## 5. Triage Agent

The Triage Agent classifies the submitted bug using available bug information.

It determines:

* Severity
* Priority
* Affected component
* Confidence
* Triage reasoning

Example:

```text
Severity: Critical
Priority: High
Component: Authentication
Confidence: 0.85
```

The agent uses keywords and bug impact information for initial classification.

---

## 6. Log Analysis Agent

The Log Analysis Agent analyzes stack traces and error logs.

It identifies:

* Exception type
* Error message
* File
* Class
* Method
* Line number
* Code path when available

Example:

```text
Exception Type: NullPointerException
File: UserService.java
Class: UserService
Method: getUserSession
Line: 45
Confidence: 0.90
```

When technical information is unavailable, the system reports it as unavailable rather than generating unsupported information.

---

## 7. Root Cause Agent

The Root Cause Agent uses submitted bug information and supporting historical evidence to determine a possible root cause.

Example:

```text
Root Cause:
A null object is likely being accessed without proper null validation.

Confidence: 0.92
```

When sufficient evidence is not available, the system returns an insufficient-evidence response instead of providing an unsupported confirmed cause.

Example:

```text
Root cause requires further analysis.

Confidence: 0.50

Insufficient evidence was available.
```

This behavior helps reduce unsupported recommendations.

---

## 8. Duplicate Detection Agent

The Duplicate Detection Agent searches the Knowledge Base for semantically similar historical defects.

The system uses vector embeddings and FAISS similarity search.

The results include:

* Bug ID
* Source
* Similarity score
* Classification
* Historical record
* Resolution information when available

Possible classifications include:

* New/Unmatched
* Related Issue
* Likely Duplicate

Example:

```text
Detection Status: Related Issue
Similarity: 72.7%
Bug ID: MOZ-001
```

---

## 9. Remediation Agent

The Remediation Agent provides a possible fix based on the available evidence.

The recommendation can use:

* Root cause reasoning
* Historical evidence
* Retrieved defects
* Technical information from the submitted bug

Example:

```text
Recommended Fix:

Add null validation before accessing the affected object.
Initialize required objects properly and handle missing
user or object data safely.

Confidence: 0.92
```

When evidence is insufficient, the system does not provide a confirmed fix.

---

## 10. Retrieval-Augmented Generation (RAG)

The platform uses a Retrieval-Augmented Generation approach to incorporate historical defect information into diagnosis.

### RAG Workflow

```text
Historical Bug Data
        |
        v
Data Preprocessing
        |
        v
Bug Text / Chunks
        |
        v
Sentence Transformer
        |
        v
Vector Embeddings
        |
        v
FAISS Vector Store
        |
        v
Semantic Retrieval
        |
        v
Relevant Historical Evidence
        |
        v
Diagnosis Agents
```

The embedding model used is:

```text
all-MiniLM-L6-v2
```

The system uses FAISS for vector similarity search.

---

## 11. Knowledge Base

The Knowledge Base contains historical software defect information used for semantic retrieval.

The stored information includes fields such as:

* Bug ID
* Source
* Component
* Severity
* Root cause
* Resolution
* Status
* Timestamp
* Text
* Chunk type
* Embedding

The FAISS vector index stores the numerical representations used for semantic search.

---

## 12. Knowledge Base Growth Mechanism — M4.2

The Knowledge Base Growth Mechanism allows resolved bugs with confirmed fixes to become future knowledge.

Before adding a bug, the system validates required information.

Required information includes:

```text
Bug ID
Component
Severity
Root Cause
Resolution
Status
```

The bug must have:

```text
Status = Resolved
```

### Validation

The system rejects:

* Missing required fields
* Empty values
* Invalid bug objects
* Bugs that are not resolved

### Duplicate Prevention

Before adding a resolved bug, the system checks whether the Bug ID already exists.

If it exists, the system prevents duplicate insertion.

### Embedding Generation

A resolved bug is converted into structured text and encoded using:

```text
all-MiniLM-L6-v2
```

The resulting embedding is added to the FAISS vector index.

Metadata is updated at the same time.

### Verification

The Knowledge Base Growth tests covered:

* Valid resolved bug
* Unresolved bug rejection
* Incomplete bug rejection
* Invalid object rejection
* Successful Knowledge Base growth
* Duplicate prevention
* Semantic retrieval

---

## 13. Defect Pattern Analytics — M4.1

The Defect Pattern Analytics Module analyzes bug records to identify recurring patterns.

The module analyzes:

* Severity
* Priority
* Component
* Exception type
* Root cause
* Duplicate status

The Streamlit analytics dashboard provides:

* KPI cards
* Severity distribution
* Component distribution
* Exception distribution
* Root cause distribution
* Duplicate-status distribution
* Filtering
* Pattern insights
* Filtered defect records

Example analysis from the tested dataset:

```text
Total Bugs: 5
Critical Bugs: 2
Affected Components: 3
Duplicate / Related: 2
```

The analytics module also identified recurring exception and root-cause patterns.

---

## 14. M4.3 End-to-End Testing

The complete pipeline was tested using multiple bug types.

### Tested Bug Categories

| Bug Type               | Exception             | Component      |
| ---------------------- | --------------------- | -------------- |
| Login/session crash    | NullPointerException  | Authentication |
| Database failure       | SQLException          | Database       |
| Payment timeout        | TimeoutException      | Payment        |
| Memory exhaustion      | OutOfMemoryError      | Memory         |
| CSV processing failure | NumberFormatException | File Upload    |

The tests covered both manually entered text and file-upload input.

---

## 15. File Upload Testing

A TXT bug report was uploaded and successfully processed.

The system correctly detected:

```text
Exception: NumberFormatException
File: FileProcessor.java
Line: 125
```

The Root Cause Agent correctly handled the case as insufficient evidence because the available information was not sufficient to confirm a specific root cause.

The Remediation Agent also returned an insufficient-evidence recommendation instead of generating an unsupported confirmed fix.

---

## 16. Related Issue Testing

A login/session bug similar to existing historical defects was submitted.

The system retrieved:

```text
Bug ID: MOZ-001
Similarity: 72.7%
Classification: Related Issue
```

The system also retrieved previously added resolved bugs from the Knowledge Base.

This demonstrated that newly added Knowledge Base records can participate in semantic retrieval.

---

## 17. Knowledge Base Performance Testing

The Knowledge Base retrieval system was tested with:

```text
Knowledge Base vectors: 22
Retrieved results: 5
```

The top retrieved result had:

```text
Similarity: 0.7509
```

The performance test confirmed that the system successfully retrieves the top 5 semantically similar defects from the Knowledge Base.

The initial measured retrieval time was:

```text
7.6160 seconds
```

This measurement includes model loading during the test run and therefore should not be interpreted as pure FAISS search time.

---

## 18. Agent Evaluation

A predefined evaluation set containing five bug scenarios was used.

Each scenario was evaluated for:

* Expected exception type
* Expected component

Results:

```text
Total Checks: 10
Passed Checks: 10
Evaluation Accuracy: 100.00%
Overall Result: PASS
```

The 100% result represents the 10 predefined checks across the five evaluation cases.

It is not intended to represent overall real-world platform accuracy.

---

## 19. Failure and Schema Handling

The platform was tested with incomplete technical information.

For example, when a stack trace contained only:

```text
SQLException: Database connection failed
```

the system reported:

```text
File: Not Available
Class: Not Available
Method: Not Available
Line: Not Available
```

Instead of inventing technical details, the system continued the diagnosis using the available evidence.

This demonstrates structured handling of incomplete bug information.

---

## 20. Technology Stack

### Programming Language

```text
Python
```

### User Interface

```text
Streamlit
```

### Data Processing

```text
Pandas
NumPy
```

### Machine Learning / Embeddings

```text
Sentence Transformers
all-MiniLM-L6-v2
```

### Vector Database / Search

```text
FAISS
```

### Visualization

```text
Plotly
```

### Development Environment

```text
Visual Studio Code
Python Virtual Environment
Git / GitHub
```

---

## 21. Project Data Flow

```text
Bug Input
   |
   v
Bug Submission
   |
   v
Orchestrator
   |
   +----> Triage Agent
   |
   +----> Log Analysis Agent
   |
   +----> Root Cause Agent
   |          |
   |          v
   |     RAG Retrieval
   |          |
   |          v
   |     Historical Evidence
   |
   +----> Duplicate Detection
   |
   +----> Remediation Agent
   |
   v
Structured Diagnosis Report
   |
   +----> Resolved Bug
   |          |
   |          v
   |     KB Growth
   |
   +----> Defect Analytics
```

---

## 22. Final Demonstration Evidence

The final testing phase demonstrated the complete diagnosis pipeline using multiple distinct bug submissions.

The demonstrated scenarios included:

1. Authentication / NullPointerException
2. Database / SQLException
3. Payment / TimeoutException
4. Memory / OutOfMemoryError
5. File Upload / NumberFormatException

The demonstration covered:

* Bug submission
* Triage
* Log analysis
* Root cause analysis
* Historical retrieval
* Duplicate detection
* Remediation
* Knowledge Base growth
* Defect analytics

---

## 23. M4 Completion Summary

### M4.1 — Defect Pattern Analytics

Status: **Completed**

Implemented:

* Defect distributions
* Recurring pattern analysis
* Component analysis
* Exception analysis
* Root-cause analysis
* Duplicate analysis
* Streamlit analytics dashboard
* Filtering and visualization

### M4.2 — Knowledge Base Growth

Status: **Completed**

Implemented:

* Resolved-bug validation
* Required-field validation
* Duplicate prevention
* Embedding generation
* FAISS vector update
* Metadata update
* Semantic retrieval verification

### M4.3 — End-to-End Testing

Status: **Completed**

Tested:

* Multiple bug types
* Multiple exception types
* Text input
* File upload
* Historical retrieval
* Related issue detection
* Insufficient evidence
* Remediation
* Knowledge Base performance
* Agent evaluation
* Failure handling

### M4.4 — Technical Documentation

Status: **In Progress**

Documentation covers:

* Architecture
* Agent workflow
* RAG
* Knowledge Base
* Knowledge Base Growth
* Defect Analytics
* Testing
* Evaluation
* Technology Stack
* Final demonstration evidence

---

## 24. Conclusion

The Intelligent Bug Diagnosis Platform provides an end-to-end workflow for automated software defect analysis.

The platform combines specialized diagnosis agents, semantic retrieval, historical defect knowledge, Knowledge Base growth, and defect analytics.

The M4 implementation extends the platform beyond individual bug diagnosis by adding recurring defect analysis, continuous Knowledge Base growth, systematic testing, evaluation, and technical documentation.

The completed testing demonstrates that the platform can process different bug types and input formats while providing structured diagnosis results, historical evidence, and remediation recommendations.
