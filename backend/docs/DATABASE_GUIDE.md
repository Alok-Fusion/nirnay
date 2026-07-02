# NIRNAY Database Guide

## Overview
The NIRNAY platform uses PostgreSQL 17 as its primary relational database. The schema is managed entirely through SQLAlchemy ORM and Alembic migrations.

## Schema Highlights
- **Users**: Extended RBAC model (Customer, Admin, Risk Analyst, etc.).
- **Accounts & Recipients**: Links users to their financial instruments. Recipient account numbers are encrypted at rest.
- **Transactions**: State machine tracking the transfer lifecycle (Initiated -> Risk Analysis -> Approved/Rejected/Awaiting Customer Decision).
- **RiskEvents**: 1-to-1 relationship with transactions, storing ML inference results (risk score, confidence, recommended action).
- **BehaviorProfiles**: Stores aggregated metrics (like average transaction amount) updated periodically.

## Migrations
Alembic is used for database migrations.

**Creating a new migration:**
```bash
alembic revision --autogenerate -m "Description of change"
```

**Applying migrations:**
```bash
alembic upgrade head
```

**Downgrading:**
```bash
alembic downgrade -1
```

## Connecting (pgAdmin)
The docker-compose setup includes pgAdmin 4 accessible at `http://localhost:5050`.
- **Email:** admin@nirnay.local
- **Password:** admin
- **Server Connection:** Use `db` as the host when adding the server in pgAdmin.
