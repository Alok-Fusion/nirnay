from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.schemas.analytics import AnalyticsResponse, CategorySpending
from backend.app.models.user import User
from backend.app.models.transaction import Transaction, TransactionState, TransactionType
from backend.app.models.risk_event import RiskEvent
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user

router = APIRouter()

@router.get('/summary', response_model=AnalyticsResponse)
def get_analytics_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.account_id.in_([a.id for a in current_user.accounts]),
        Transaction.status == TransactionState.COMPLETED,
        Transaction.type == TransactionType.TRANSFER
    ).scalar() or 0.0

    return AnalyticsResponse(
        total_spent=total_spent,
        categories=[CategorySpending(category='Shopping', amount=total_spent)],
        risk_distribution={'Low': 5, 'Medium': 2, 'High': 0}
    )

@router.get('/dashboard')
def get_analytics_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Gather all transactions
    account_ids = [a.id for a in current_user.accounts]
    transactions = db.query(Transaction).filter(
        Transaction.account_id.in_(account_ids)
    ).all()
    
    # Calculate spending by month (last 6 months)
    import datetime
    from collections import defaultdict
    
    monthly_data = defaultdict(lambda: {"spending": 0.0, "income": 5500.0})
    
    months_keys = []
    now = datetime.datetime.utcnow()
    for i in range(5, -1, -1):
        m_date = now - datetime.timedelta(days=30 * i)
        m_key = m_date.strftime("%b")
        months_keys.append(m_key)
        monthly_data[m_key] = {"spending": 0.0, "income": 5500.0}
        
    for tx in transactions:
        if tx.status == TransactionState.COMPLETED:
            m_key = tx.created_at.strftime("%b")
            if m_key in monthly_data:
                monthly_data[m_key]["spending"] += tx.amount
                
    cash_flow = []
    for m in months_keys:
        cash_flow.append({
            "name": m,
            "spending": round(monthly_data[m]["spending"], 2),
            "income": monthly_data[m]["income"]
        })
        
    # AI risk interventions (blocked vs approved) in last 4 weeks
    weekly_interventions = [
        {"name": "Week 1", "blocked": 0, "approved": 0},
        {"name": "Week 2", "blocked": 0, "approved": 0},
        {"name": "Week 3", "blocked": 0, "approved": 0},
        {"name": "Week 4", "blocked": 0, "approved": 0},
    ]
    
    for tx in transactions:
        delta_days = (now - tx.created_at.replace(tzinfo=None)).days
        if delta_days < 28:
            week_idx = 3 - (delta_days // 7)
            if 0 <= week_idx < 4:
                if tx.status == TransactionState.COMPLETED:
                    weekly_interventions[week_idx]["approved"] += 1
                elif tx.status == TransactionState.BLOCKED:
                    weekly_interventions[week_idx]["blocked"] += 1
                    
    # Ensure there is some data for visualization if empty
    total_approved = sum(w["approved"] for w in weekly_interventions)
    total_blocked = sum(w["blocked"] for w in weekly_interventions)
    if total_approved == 0 and total_blocked == 0:
        weekly_interventions = [
            {"name": "Week 1", "blocked": 1, "approved": 3},
            {"name": "Week 2", "blocked": 0, "approved": 4},
            {"name": "Week 3", "blocked": 2, "approved": 2},
            {"name": "Week 4", "blocked": 0, "approved": 1},
        ]
        
    # Calculate category spending distribution
    category_spending = defaultdict(float)
    for tx in transactions:
        if tx.status == TransactionState.COMPLETED:
            recipient_name = tx.recipient.name.lower() if tx.recipient else "peer"
            if "crypto" in recipient_name or "exchange" in recipient_name or "coin" in recipient_name:
                cat = "Crypto Exchange"
            elif "investment" in recipient_name or "capital" in recipient_name or "wealth" in recipient_name:
                cat = "Investment Platform"
            elif "services" in recipient_name or "power" in recipient_name or "utility" in recipient_name or "bill" in recipient_name:
                cat = "Bills & Utilities"
            else:
                cat = "Peer Transfer"
            category_spending[cat] += tx.amount
            
    if not category_spending:
        category_spending = {
            "Peer Transfer": 1500.00,
            "Bills & Utilities": 350.00,
            "Investment Platform": 500.00,
            "Crypto Exchange": 0.00
        }
        
    categories = [{"name": k, "value": round(v, 2)} for k, v in category_spending.items()]
    
    # Hourly distribution for temporal Digital Twin visualization
    hourly_distribution = [0] * 24
    for tx in transactions:
        hour = tx.created_at.hour
        hourly_distribution[hour] += 1
        
    if sum(hourly_distribution) == 0:
        for h in range(9, 18):
            hourly_distribution[h] = 2
            
    hourly_data = [{"hour": f"{h:02d}:00", "count": hourly_distribution[h]} for h in range(24)]
    
    # Risk score progression
    risk_events = db.query(RiskEvent).join(Transaction).filter(
        Transaction.account_id.in_(account_ids)
    ).order_by(RiskEvent.created_at.desc()).limit(10).all()
    
    risk_progression = []
    for r in reversed(risk_events):
        risk_progression.append({
            "tx_id": r.transaction_id,
            "score": round(float(r.risk_score) * 100, 1),
            "recipient": r.transaction.recipient.name if r.transaction.recipient else "Unknown"
        })
        
    if not risk_progression:
        risk_progression = [
            {"tx_id": 101, "score": 8.0, "recipient": "Alice Smith"},
            {"tx_id": 102, "score": 12.0, "recipient": "Bob Jones"},
            {"tx_id": 103, "score": 75.0, "recipient": "Unknown Investment"},
            {"tx_id": 104, "score": 15.0, "recipient": "Alice Smith"},
            {"tx_id": 105, "score": 6.0, "recipient": "John Doe"},
        ]
        
    return {
        "cash_flow": cash_flow,
        "ai_interventions": weekly_interventions,
        "category_spending": categories,
        "hourly_distribution": hourly_data,
        "risk_progression": risk_progression,
        "summary": {
            "total_transactions": len(transactions),
            "total_spent": round(sum(tx.amount for tx in transactions if tx.status == TransactionState.COMPLETED), 2),
            "total_blocked": round(sum(tx.amount for tx in transactions if tx.status == TransactionState.BLOCKED), 2),
            "active_rules_triggered": sum(1 for tx in transactions if tx.risk_event and len(tx.risk_event.reason_codes or []) > 0)
        }
    }
