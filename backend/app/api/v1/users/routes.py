from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.schemas.user import UserResponse
from backend.app.models.user import User
from backend.app.database.session import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.repositories.user_repo import user_repo

router = APIRouter()

@router.get('/me', response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get('/security')
def get_user_security(current_user: User = Depends(get_current_user)):
    # Calculate mock metrics based on real user data or return static values for MVP
    return {
        "overallScore": 92,
        "trustedDevices": 1,
        "blockedAttempts": 0,
        "lastLogin": current_user.created_at.isoformat(),
        "activeAlerts": 0
    }

@router.get('/me/behavior')
def get_user_behavior(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from backend.app.models.behavior_profile import BehaviorProfile
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == current_user.id).first()
    
    if not profile:
        # Create default profile if somehow missing
        profile = BehaviorProfile(
            user_id=current_user.id,
            avg_transaction_amount=0.0,
            transaction_count=0,
            average_daily_transactions=0.0,
            trusted_recipients=[],
            known_devices=[],
            known_locations=[],
            average_balance=0.0,
            historical_risk=0.0,
            trust_score=50,
            trust_level="NEW"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
    return {
        "avg_transaction_amount": profile.avg_transaction_amount,
        "transaction_count": profile.transaction_count,
        "average_daily_transactions": profile.average_daily_transactions,
        "preferred_transfer_hour": profile.preferred_transfer_hour,
        "trusted_recipients": profile.trusted_recipients or [],
        "known_devices": profile.known_devices or [],
        "known_locations": profile.known_locations or [],
        "average_balance": profile.average_balance,
        "historical_risk": profile.historical_risk,
        "trust_score": profile.trust_score,
        "trust_level": profile.trust_level,
        "last_updated": profile.last_updated.isoformat() if profile.last_updated else None
    }

@router.post('/me/behavior/upload-statement')
def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import csv
    import json
    import io
    from datetime import datetime
    from backend.app.models.recipient import Recipient
    from backend.app.models.transaction import Transaction, TransactionState, TransactionType
    from backend.app.models.behavior_profile import BehaviorProfile
    
    content = file.file.read()
    filename = file.filename.lower()
    
    transactions_to_create = []
    
    try:
        if filename.endswith('.json'):
            data = json.loads(content.decode('utf-8'))
            if not isinstance(data, list):
                raise HTTPException(status_code=400, detail="JSON must be a list of transactions")
            for item in data:
                transactions_to_create.append({
                    "amount": float(item.get("amount", 0)),
                    "recipient_name": str(item.get("recipient_name", "Unknown")),
                    "recipient_account": str(item.get("recipient_account", "0000")),
                    "bank_code": str(item.get("bank_code", "GEN001")),
                    "date": datetime.fromisoformat(item.get("date")) if item.get("date") else datetime.utcnow()
                })
        elif filename.endswith('.csv'):
            csv_text = content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(csv_text))
            for row in reader:
                row_clean = {k.lower().strip(): v for k, v in row.items()}
                amount_val = row_clean.get("amount") or row_clean.get("amount(usd)") or 0
                transactions_to_create.append({
                    "amount": float(amount_val),
                    "recipient_name": str(row_clean.get("recipient_name") or row_clean.get("recipient") or "Unknown"),
                    "recipient_account": str(row_clean.get("recipient_account") or row_clean.get("account") or "0000"),
                    "bank_code": str(row_clean.get("bank_code") or row_clean.get("bank") or "GEN001"),
                    "date": datetime.fromisoformat(row_clean.get("date")) if row_clean.get("date") else datetime.utcnow()
                })
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse statement: {str(e)}")
        
    if not transactions_to_create:
        raise HTTPException(status_code=400, detail="No transactions found in file.")
        
    # Get user's primary account
    account = current_user.accounts[0] if current_user.accounts else None
    if not account:
        raise HTTPException(status_code=400, detail="User has no accounts to link transactions.")
        
    imported_count = 0
    for tx_data in transactions_to_create:
        recipient = db.query(Recipient).filter(
            Recipient.user_id == current_user.id,
            Recipient.account_number == tx_data["recipient_account"]
        ).first()
        
        if not recipient:
            recipient = Recipient(
                user_id=current_user.id,
                account_number=tx_data["recipient_account"],
                bank_code=tx_data["bank_code"],
                name=tx_data["recipient_name"],
                is_trusted=False
            )
            db.add(recipient)
            db.flush()
            
        db_tx = Transaction(
            account_id=account.id,
            recipient_id=recipient.id,
            amount=tx_data["amount"],
            currency="USD",
            status=TransactionState.COMPLETED,
            type=TransactionType.TRANSFER,
            created_at=tx_data["date"],
            updated_at=tx_data["date"]
        )
        db.add(db_tx)
        imported_count += 1
        
    db.commit()
    
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.user_id == current_user.id).first()
    if not profile:
        profile = BehaviorProfile(user_id=current_user.id)
        db.add(profile)
        db.flush()
        
    all_completed_txs = db.query(Transaction).filter(
        Transaction.account_id == account.id,
        Transaction.status == TransactionState.COMPLETED
    ).all()
    
    count = len(all_completed_txs)
    if count > 0:
        total_amount = sum(tx.amount for tx in all_completed_txs)
        profile.transaction_count = count
        profile.avg_transaction_amount = total_amount / count
        
        days = max(1, (datetime.utcnow() - current_user.created_at.replace(tzinfo=None)).days) if current_user.created_at else 1
        profile.average_daily_transactions = count / float(days)
        
        hours = [tx.created_at.hour for tx in all_completed_txs]
        profile.preferred_transfer_hour = max(set(hours), key=hours.count)
        
        known_locs = list(profile.known_locations or [])
        if "Imported Statement" not in known_locs:
            known_locs.append("Imported Statement")
            profile.known_locations = known_locs
            
        known_devs = list(profile.known_devices or [])
        if "System File" not in known_devs:
            known_devs.append("System File")
            profile.known_devices = known_devs
            
        rec_ids = list(profile.trusted_recipients or [])
        for tx in all_completed_txs:
            if tx.recipient_id and tx.recipient_id not in rec_ids:
                rec_ids.append(tx.recipient_id)
        profile.trusted_recipients = rec_ids
        
        if count <= 5:
            profile.trust_level = "NEW"
            profile.trust_score = int(50 + (count * 3))
        elif count <= 20:
            profile.trust_level = "LEARNING"
            profile.trust_score = int(65 + ((count - 5) * 0.8))
        elif count <= 100:
            profile.trust_level = "ESTABLISHED"
            profile.trust_score = int(77 + ((count - 20) * 0.2))
        else:
            profile.trust_level = "TRUSTED"
            profile.trust_score = min(99, int(93 + ((count - 100) * 0.05)))
            
    db.commit()
    db.refresh(profile)
    
    return {
        "message": f"Successfully parsed and seeded {imported_count} transactions.",
        "imported_count": imported_count,
        "trust_score": profile.trust_score,
        "trust_level": profile.trust_level,
        "transaction_count": profile.transaction_count
    }
