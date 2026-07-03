<div align="center">

# 🏦 NIRNAY

### AI-Powered Financial Decision Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-FF6B6B?style=for-the-badge&logo=openai&logoColor=white)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **NIRNAY** *(Hindi: Decision)* is an **AI-Powered Financial Decision Intelligence Platform** that transforms traditional fraud detection into autonomous, explainable, and customer-centric decision making.
>
> By combining Machine Learning, Rule-Based Banking Policies, Contextual Reasoning, and Conversational AI, it evaluates every transaction before execution — understanding **intent rather than just risk** — and recommends the safest course of action. It protects customers from modern financial scams while preserving a seamless banking experience.

</div>

---

## 🌟 What Makes NIRNAY Different

Unlike demo applications that fake AI with hardcoded responses, NIRNAY is a **real enterprise system**:

- 🤖 **No Fake AI** — Every transaction runs through a live ML model, real rule engine, and LangGraph agent graph
- 🗄️ **No Mock Data** — The frontend is strictly driven by the PostgreSQL database. Zero hardcoded state
- 🔒 **No Bypassed Security** — Step-Up Authentication is enforced as the final barrier before any funds move
- 📊 **No Manual Refreshes** — React Query cache invalidation propagates every backend change to the UI automatically
- 🏛️ **No Monolithic Logic** — Every concern (Orchestration, ML, Rules, AI Agents, Decision, Audit) has its own layer

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   NIRNAY Platform                           │
│                                                             │
│  React 18 + Vite + MUI + React Query                       │
│           │                                                 │
│           ▼                                                 │
│  FastAPI  ──►  TransactionOrchestrator                     │
│                      │                                      │
│            ┌─────────┼─────────┐                           │
│            ▼         ▼         ▼                           │
│       Validation   Feature   Rule Engine                   │
│                   Generator                                 │
│                      │                                      │
│                      ▼                                      │
│                  ML Engine (XGBoost/SHAP)                  │
│                      │                                      │
│             ┌────────┴────────┐                            │
│      SAFE ──┘                 └──► LangGraph Multi-Agent   │
│             │                      ├─ ContextAgent         │
│             │                      ├─ RiskAgent            │
│             │                      ├─ PolicyAgent          │
│             │                      └─ DecisionAgent        │
│             │                           │                  │
│             └──────────────────────────►│                  │
│                                   Decision Engine          │
│                                         │                  │
│                            Step-Up Authentication          │
│                                         │                  │
│                                   Ledger Execution         │
│                                         │                  │
│                         Audit ─── Analytics ─── Notify    │
│                                                             │
│  PostgreSQL 17 (Docker)  ←────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Transaction Decision Pipeline

Every transfer triggers an **immutable, sequential pipeline**:

| Stage | Component | Description |
|-------|-----------|-------------|
| 1 | **Validation** | Balance check, recipient validation, schema verification |
| 2 | **Customer Context** | Build behavioral profile from 90-day history |
| 3 | **Feature Engineering** | 30+ live SQL-derived ML features (velocity, network, amount ratios) |
| 4 | **ML Analysis** | XGBoost risk scoring with SHAP explainability |
| 5 | **Rule Engine** | Deterministic hard rules (crypto blocks, velocity limits, blacklists) |
| 6 | **AI Analysis** | LangGraph multi-agent graph (triggered only for suspicious cases) |
| 7 | **Decision Engine** | Synthesizes all signals into final: APPROVE / ESCALATE / BLOCK |
| 8 | **Step-Up Auth** | Customer re-authentication before ledger commitment |
| 9 | **Execution** | Atomic ledger debit/credit with rollback safety |
| 10 | **Propagation** | Dashboard, History, Analytics, Security all updated automatically |

---

## 📁 Project Structure

```
nirnay/
├── ai/                          # AI & Intelligence Layer
│   ├── agents/                  # LangGraph Agents
│   │   ├── context_agent.py     # Customer context intelligence
│   │   ├── risk_agent.py        # ML risk interpretation
│   │   ├── policy_agent.py      # Policy & compliance agent
│   │   └── decision_agent.py    # Final decision synthesis
│   ├── decision/                # Decision Engine
│   │   └── engine.py
│   ├── memory/                  # FAISS Vector Memory
│   ├── orchestrator/            # LangGraph Graph Definition
│   │   └── graph.py
│   ├── schemas/                 # AI Layer Schemas
│   ├── llm_manager.py           # LLM Provider Fallback (Groq → OpenAI → Ollama)
│   └── registry/                # LLM Factory
│
├── backend/
│   └── app/
│       ├── ai/
│       │   ├── decision/
│       │   │   └── rule_engine.py       # Deterministic Rule Engine
│       │   └── features/
│       │       └── generator.py         # Live SQL Feature Engineering
│       ├── api/v1/                      # REST API Routes
│       │   ├── auth/                    # JWT Authentication
│       │   ├── accounts/                # Account Management
│       │   ├── transactions/            # Transfer Workflow
│       │   ├── recipients/              # Recipient Management
│       │   ├── analytics/               # Analytics Dashboard
│       │   ├── risk/                    # Risk History & Metrics
│       │   └── system/                  # Health & Metrics Endpoints
│       ├── middleware/                  # Rate Limiter, Request Context
│       ├── models/                      # SQLAlchemy ORM Models
│       ├── repositories/               # Repository Pattern (base.py)
│       ├── schemas/                     # Pydantic Validation Schemas
│       ├── services/
│       │   ├── transaction_orchestrator.py  # 🧠 Core State Machine
│       │   ├── auth_service.py
│       │   └── ml_service.py           # Risk Inference Engine
│       └── main.py                     # FastAPI Application Entry Point
│
├── frontend/
│   └── src/
│       ├── features/
│       │   ├── authentication/         # Login Screen
│       │   ├── dashboard/              # Command Center
│       │   ├── transfers/              # Transfer Flow + Decision Details
│       │   ├── transactions/           # History + Recipient Management
│       │   ├── analytics/              # Analytics Dashboard
│       │   ├── security/               # Security Center
│       │   └── settings/               # Profile Settings
│       ├── services/
│       │   ├── api.ts                  # Axios Instance (JWT interceptors)
│       │   └── apiHooks.ts             # React Query Hooks (Live Backend)
│       ├── contexts/                   # Auth Context
│       ├── guards/                     # Route Guards (AuthGuard, GuestGuard)
│       └── routes/                     # React Router Configuration
│
├── ml/                          # ML Pipeline & Model Registry
├── datasets/                    # Training Data
├── tests/                       # Backend Test Suites
├── scripts/                     # Utility Scripts (seed, etc.)
├── docker-compose.yml           # PostgreSQL + pgAdmin
├── start_nirnay.py              # 🚀 One-Click Local Launcher
├── requirements.txt             # Python Dependencies
└── alembic.ini                  # Database Migration Config
```

---

## ⚡ Quick Start

### Prerequisites

| Requirement | Version | Install |
|-------------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Docker Desktop | Latest | [docker.com](https://docker.com) |
| Git | Latest | [git-scm.com](https://git-scm.com) |

---

### 1. Clone the Repository

```bash
git clone https://github.com/Alok-Fusion/nirnay.git
cd nirnay
```

### 2. Start PostgreSQL (Docker)

```bash
docker-compose up -d
```

This starts PostgreSQL 17 on `localhost:5432` and pgAdmin on `localhost:5050`.

### 3. Create Python Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# LLM Provider (required for AI Analysis on suspicious transactions)
GROQ_API_KEY=your_groq_api_key_here       # Free at console.groq.com
# OPENAI_API_KEY=your_openai_key_here     # Optional fallback

# PostgreSQL (matches docker-compose.yml defaults)
POSTGRES_USER=nirnay_user
POSTGRES_PASSWORD=nirnay_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nirnay_db

# Security
SECRET_KEY=your_very_long_random_secret_key_here
```

> **Free LLM Key**: Get a free Groq API key at [console.groq.com](https://console.groq.com). It runs Llama3-70b at 500 tokens/second for free.

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 8. Seed Demo User (Optional but Recommended)

```bash
python scripts/seed_demo_user.py
```

This creates a demo banking account with:
- **Email**: `alok@example.com`
- **Password**: `password`
- Sample recipients and transaction history

### 9. Launch Everything

```bash
python start_nirnay.py
```

This unified launcher will:
- ✅ Verify `.env` configuration
- ✅ Test PostgreSQL connectivity
- ✅ Start the FastAPI backend on `http://localhost:8000`
- ✅ Start the React frontend on `http://localhost:5173`
- ✅ Display real-time system health

Or launch manually in two terminals:

```bash
# Terminal 1 — Backend
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

---

## 🖥️ Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | React Banking Dashboard |
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Swagger Interactive Docs |
| **System Health** | http://localhost:8000/api/v1/system/health | Health Check JSON |
| **System Metrics** | http://localhost:8000/api/v1/system/metrics | Metrics JSON |
| **pgAdmin** | http://localhost:5050 | Database Management UI |

---

## 🤖 AI Decision Engine

### LLM Fallback Strategy

NIRNAY implements a resilient multi-provider LLM strategy:

```
Groq (Primary)  →  OpenAI (Secondary)  →  Ollama (Local Fallback)  →  ML-Only Decision
```

If all LLM providers fail, the system gracefully falls back to pure ML + Rule Engine decision making — **zero downtime, zero broken transactions**.

### LangGraph Multi-Agent Graph

The LangGraph system only activates for **SUSPICIOUS** transactions (those that pass basic rules but need deeper AI analysis):

```
ContextIntelligenceAgent
    └── Builds 360° customer profile from DB history

RiskAssessmentAgent
    └── Interprets ML scores + SHAP feature importance

PolicyComplianceAgent
    └── Cross-references regulatory rules & scam patterns

DecisionSynthesisAgent
    └── Produces final verdict with evidence report
```

### Rule Engine (Hard Rules)

Deterministic rules that cannot be overridden by AI:
- 🔴 **HARD BLOCK**: Crypto wallet transfers over ₹50,000
- 🔴 **HARD BLOCK**: Blacklisted accounts
- 🔴 **HARD BLOCK**: Velocity > 10 transactions/hour
- 🟡 **SUSPICIOUS**: New recipient + large amount → AI Analysis
- 🟡 **SUSPICIOUS**: After-hours high-value transfer
- 🟢 **SAFE**: Trusted recipient + amount within normal range → Direct Auth

---

## 🔒 Security Architecture

| Security Layer | Implementation |
|----------------|----------------|
| **Authentication** | JWT Access Tokens (30 min) + Refresh Tokens (7 days) |
| **Step-Up Auth** | Required for every single fund movement |
| **Rate Limiting** | Per-IP sliding window middleware |
| **CORS** | Configurable origin whitelist |
| **Input Validation** | Pydantic strict typing on all endpoints |
| **Output Sanitization** | No stack traces exposed in production responses |
| **Audit Logging** | Every action logged with Correlation ID, User ID, Risk Score |
| **Ownership Validation** | Users can only access their own accounts/transactions |

---

## 📊 System Health & Metrics

### `GET /api/v1/system/health`
```json
{
  "status": "healthy",
  "database": "healthy",
  "ml_model": "loaded",
  "rule_engine": "loaded",
  "langgraph": "loaded",
  "llm_provider": { "status": "healthy", "provider": "groq", "latency_ms": 12 },
  "decision_engine": "loaded",
  "memory": "active",
  "latency_ms": 45.2
}
```

### `GET /api/v1/system/metrics`
```json
{
  "total_transactions": 142,
  "blocked_transfers": 18,
  "ai_interventions": 23,
  "average_risk_score": 0.24,
  "average_ml_time_ms": 45.2,
  "average_ai_time_ms": 1200.5,
  "average_decision_time_ms": 15.0,
  "database_connections": 5
}
```

---

## 🧪 Running Tests

### Backend Tests

```bash
# From the project root with venv activated
$env:PYTHONPATH="c:\path\to\nirnay"  # Windows PowerShell
# OR
export PYTHONPATH=$(pwd)             # macOS/Linux

pytest tests/
```

### Frontend Build Verification

```bash
cd frontend
npm run build
```

---

## 🎯 Enterprise Test Scenarios

| Scenario | Flow | Expected Outcome |
|----------|------|-----------------|
| **Trusted Recipient** | ₹500 → known contact | Auto-approve → Auth → Complete |
| **Normal Transfer** | ₹10,000 → known recipient | ML low risk → Auth → Complete |
| **New Recipient Large** | ₹25,000 → new contact | AI Analysis → Conversation → Auth → Complete |
| **Crypto Block** | Any → crypto wallet | Hard block by Rule Engine |
| **High Velocity** | >10 tx/hour | Hard block by Rule Engine |
| **LLM Offline** | System degraded | Fallback to ML decision → Continue |
| **JWT Expired** | Token expires | Auto-refresh via interceptor → Continue |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async REST API framework |
| **SQLAlchemy** | ORM with Alembic migrations |
| **PostgreSQL 17** | Primary datastore (Docker) |
| **Pydantic v2** | Strict request/response validation |
| **LangGraph** | Multi-agent orchestration graph |
| **LangChain** | LLM abstraction layer |
| **XGBoost** | Risk scoring ML model |
| **SHAP** | ML explainability |
| **FAISS** | Vector similarity memory |
| **JWT** | Stateless authentication |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | Component framework |
| **Vite** | Ultra-fast build tooling |
| **TypeScript** | Strict type safety |
| **Material UI v6** | Enterprise component library |
| **React Query** | Server state management + cache invalidation |
| **React Router v6** | Client-side routing |
| **Framer Motion** | Micro-animations |
| **Axios** | HTTP client with JWT interceptors |

---

## 📝 API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Create new account |
| `POST` | `/api/v1/auth/login` | Login (returns JWT) |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/transactions/transfer` | Initiate transfer → runs full pipeline |
| `POST` | `/api/v1/transactions/{id}/authenticate` | Step-up auth → execute ledger |
| `GET` | `/api/v1/transactions/history` | Paginated transaction history |

### Account & Recipients
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/accounts/summary` | Balance + account overview |
| `GET` | `/api/v1/recipients` | All saved recipients |
| `POST` | `/api/v1/recipients` | Add new recipient |

### Risk & Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/risk/history` | Full risk event log |
| `GET` | `/api/v1/analytics/dashboard` | Dashboard aggregates |
| `GET` | `/api/v1/system/health` | System health status |
| `GET` | `/api/v1/system/metrics` | Aggregate metrics |

---

## 🌐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Recommended | LLM primary provider (free) |
| `OPENAI_API_KEY` | Optional | LLM secondary fallback |
| `POSTGRES_USER` | Yes | DB username (default: `nirnay_user`) |
| `POSTGRES_PASSWORD` | Yes | DB password (default: `nirnay_password`) |
| `POSTGRES_SERVER` | Yes | DB host (default: `localhost`) |
| `POSTGRES_PORT` | Yes | DB port (default: `5432`) |
| `POSTGRES_DB` | Yes | DB name (default: `nirnay_db`) |
| `SECRET_KEY` | Yes | JWT signing secret (change in production!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT expiry (default: `30`) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | Refresh token expiry (default: `7`) |

---

## 🔬 Feature Engineering (30+ ML Features)

The `FeatureGenerator` extracts the following from live database queries:

- **Velocity Features**: tx count (1h, 24h, 7d), amount sum, average
- **Recipient Features**: is_new_recipient, is_trusted, past_tx_count
- **Time Features**: hour_of_day, is_weekend, is_after_hours
- **Amount Features**: amount_vs_avg_ratio, is_round_number, is_large_transfer
- **Network Features**: unique_recipients_7d, cross_bank_ratio
- **Risk Features**: prior_blocked_count, prior_ml_risk_avg, fraud_velocity_score

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for enterprise banking that takes AI seriously.**

*NIRNAY — Because every financial decision deserves real intelligence.*

</div>
