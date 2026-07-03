# Multi-Agent Decision Intelligence Architecture

## Overview
The AI Layer for NIRNAY implements a LangGraph-based Multi-Agent system to reason over ML risk predictions and provide explainable, policy-driven financial decisions with human-in-the-loop capabilities.

## Agents

### 1. Context Intelligence Agent
- **Role**: Data Aggregator
- **Responsibility**: Collects data from PostgreSQL (Customer Profile, Behavior Profile) and the ML Service (Risk Score, SHAP values). Normalizes it into a unified `DecisionContext`.

### 2. Risk Interpretation Agent
- **Role**: Explainer
- **Responsibility**: Translates raw ML reason codes and SHAP values into human-readable evidence using an LLM. Outputs an `EvidenceReport`.

### 3. Policy & Compliance Agent
- **Role**: Rule Enforcer
- **Responsibility**: Compares the `DecisionContext` and `EvidenceReport` against business rules to generate a `PolicyDecision` (Approve, Escalate, Require Human Approval).

### 4. Conversation Orchestrator
- **Role**: Customer Interface
- **Responsibility**: Evaluates the `PolicyDecision` and history to determine whether to ask the user a question, explain a delay, or recommend an action. Outputs a `ConversationAction`.

### 5. Memory Agent
- **Role**: State Persistence
- **Responsibility**: Updates the FAISS vector store with the outcome of the transaction, creating a long-term memory trace for future interactions.

## Orchestration (LangGraph)
- **State**: The workflow revolves around a strongly-typed `DecisionState` passing context, evidence, and policy decisions between nodes.
- **Checkpointing**: Uses `MemorySaver` to checkpoint state. If the Policy Agent requires customer confirmation, the graph suspends execution at the `HumanApproval` node, waits for input via the CLI or REST API, and resumes gracefully.

## Observability
- All agents use the `@trace_agent` decorator, pushing their execution durations, statuses, and errors into the `DecisionState`'s `audit_trail` for real-time observability.
