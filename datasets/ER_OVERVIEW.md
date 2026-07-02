# NIRNAY - Entity Relationship Overview

## Core Entities
- **Customers** (1) --- (1..N) **Accounts**
- **Customers** (1) --- (1..N) **Recipients**
- **Customers** (1) --- (1) **Behavior Profiles**

## Transactions & Intelligence
- **Transactions** (N) --- (1) **Customers**
- **Transactions** (N) --- (1) **Accounts**
- **Transactions** (N) --- (0..1) **Recipients**
- **Transactions** (N) --- (0..1) **Merchants**
- **Risk Events** (1) --- (1) **Transactions**
- **Conversations** (N) --- (1) **Transactions**
- **Feedback** (1) --- (1) **Transactions**

## Reference
- **Merchants** (1) --- (1) **Merchant Reputation**
- **Risk Events** (N) --- (1) **Scam Patterns**
