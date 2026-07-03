# NIRNAY - Agentic Architecture

The NIRNAY Agentic AI Platform utilizes a modular, multi-agent architecture powered by LangGraph to process financial transactions, detect fraud, evaluate policies, and orchestrate customer interactions.

## 1. Context Intelligence Agent
**Role:** Data Aggregator & Feature Engineer
**Input:** Raw transaction payload and Customer ID
**Responsibilities:**
- Fetches static and dynamic customer profiles.
- Validates merchant and recipient identities.
- Calls the underlying Machine Learning (LightGBM) model to generate Risk Scores and SHAP values.
- Retrieves `Past Customer Memory Context` from the FAISS vector database.

## 2. Risk Interpretation Agent
**Role:** Explainability Engine
**Input:** Raw ML Risk Scores and SHAP values
**Responsibilities:**
- Translates technical ML outputs into human-readable evidence.
- Explains *why* a transaction was flagged, citing specific feature deviations (e.g., "The amount is 3x higher than average").
- Identifies potential scam typologies (e.g., Romance Scam, Pig Butchering).

## 3. Policy & Compliance Agent (Recommendation Engine)
**Role:** Business Logic Evaluator
**Input:** Context Profile and Evidence Report
**Responsibilities:**
- Validates the context against bank baseline rules.
- Determines the required action (e.g., Approve, Require Customer Confirmation, Delay).
- Generates prioritized Contextual Recommendations (e.g., "Cancel Transaction", "Verify Exchange").
- Calculates AI Confidence Metrics (Overall, Decision, Memory, Recommendation).

## 4. Conversation Orchestrator
**Role:** Customer Interaction & Financial Advisor
**Input:** Context, Evidence, Policy, and Past Customer Memory
**Responsibilities:**
- Evaluates the current state of the conversation.
- Employs strict "Decisive" logic: Immediately ends workflows upon explicit user authorization/cancellation without repetitive confirmation loops.
- Acts as a Financial Advisor: If a user blindly authorizes a high-risk transfer, it educates them on the risk indicators and presents recommendations.
- Validates active memory: Leverages past interactions to warn users about previously rejected recipients.

## 5. Memory Agent
**Role:** Persistent Intelligence
**Input:** Completed Transaction Context and Final Decision
**Responsibilities:**
- Saves the full contextual summary of the transaction to a FAISS vector database.
- Embeds the customer's decision (e.g., "Authorized", "Rejected") so future transactions to the same entity benefit from historical knowledge.
