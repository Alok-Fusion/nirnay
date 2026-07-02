# NIRNAY API Reference

This document provides a high-level overview of the API endpoints available in the NIRNAY backend platform.

For a fully interactive, up-to-date OpenAPI documentation (Swagger UI), start the server and navigate to `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

## Base URL
All API v1 endpoints are prefixed with `/api/v1`.

## Authentication `(/api/v1/auth)`
- `POST /register`: Register a new user (Customer by default).
- `POST /login`: Authenticate via username (email) and password to receive a JWT access token and refresh token.

## Users `(/api/v1/users)`
- `GET /me`: Retrieve the authenticated user's profile and RBAC role.

## Accounts `(/api/v1/accounts)`
- `GET /summary`: Retrieve all active accounts belonging to the authenticated customer, including balances and account numbers.

## Transactions `(/api/v1/transactions)`
- `POST /transfer`: Initiate a money transfer. This triggers the ML Risk Inference Engine and returns a composite response containing the transaction state, the risk assessment, and any required actions (e.g., AWAITING_CUSTOMER_DECISION).

## Recipients `(/api/v1/recipients)`
- `GET /`: List all saved recipients for the current user.
- `POST /`: Add a new recipient (account number is stored encrypted).

## Risk `(/api/v1/risk)`
- `GET /history`: List all risk events associated with the current user's past transactions.
- `GET /report/{transaction_id}`: Retrieve a detailed risk report for a specific transaction (includes confidence score, recommended action, and features).

## Analytics `(/api/v1/analytics)`
- `GET /summary`: Retrieve aggregated spending metrics, category breakdown, and personal risk distribution for the customer dashboard.

## Admin `(/api/v1/admin)`
*Requires `Admin` RBAC role.*
- `GET /customers`: List all registered customers.
- `GET /system-stats`: Retrieve high-level system statistics (e.g., total active users, system health).
