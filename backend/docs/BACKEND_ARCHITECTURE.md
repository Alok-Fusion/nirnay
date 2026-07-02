# NIRNAY Backend Architecture

## Overview
The NIRNAY backend is built with FastAPI, adhering to a layered architecture approach (Routes -> Services -> Repositories -> Models) to separate concerns and improve testability and maintainability. It seamlessly integrates with the Phase 2 ML Decision Engine (`ml.inference.RiskInferenceEngine`) to provide real-time risk assessment on transactions.

## Technologies
- **Framework:** FastAPI
- **Database:** PostgreSQL (using Docker Compose)
- **ORM:** SQLAlchemy (with Alembic for migrations)
- **Validation:** Pydantic
- **Security:** Argon2id (password hashing), JWT (authentication), `sqlalchemy-utils` (field encryption)

## Security Architecture
The platform is designed with a "security-first" approach:
1. **Password Hashing:** Argon2id is used via `passlib`, preventing rainbow table and brute-force attacks.
2. **Authentication:** Short-lived JWT Access Tokens combined with longer-lived Refresh Tokens.
3. **Data at Rest:** Highly sensitive fields (e.g., `Recipient.account_number`) are stored using an encrypted type (`AesEngine`, `pkcs5`).
4. **Rate Limiting:** A custom middleware restricts incoming requests to mitigate DDoS and brute-force attempts.
5. **Observability & Traceability:** Every request receives an `X-Correlation-ID`. Audit logs track user actions in the database.

## Request Flow (Example: Money Transfer)
1. **API Router:** `POST /api/v1/transactions/transfer` receives the Pydantic-validated request.
2. **TransactionService:** 
   - Validates the sender's balance and recipient validity.
   - Saves a new transaction in the `INITIATED` state.
   - Collects ML feature data (e.g., balance, time, recipient trustworthiness).
   - Calls the `ml_service.analyze_transaction()`.
3. **ML Service:** Wraps the `RiskInferenceEngine`, invoking SHAP explainer and model predict logic.
4. **TransactionService:** 
   - Based on ML results, sets transaction state to `APPROVED`, `AWAITING_CUSTOMER_DECISION`, or `REJECTED`.
   - Records the `RiskEvent` in the database.
   - Updates account balances if approved.
5. **API Router:** Returns a structured JSON response containing the decision and risk factors.
