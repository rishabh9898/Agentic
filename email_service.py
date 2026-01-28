# ================================
# FastAPI Email Service Backend
# ================================

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from models import Email, get_db, Base, engine, INITIAL_EMAILS
from schemas import EmailCreate, EmailResponse

app = FastAPI(title="Email Service API", version="1.0.0")


# ================================
# Helper Functions
# ================================

def seed_database(db: Session):
    """Seed the database with initial emails."""
    for email_data in INITIAL_EMAILS:
        existing = db.query(Email).filter(Email.id == email_data["id"]).first()
        if not existing:
            email = Email(
                id=email_data["id"],
                sender=email_data["sender"],
                recipient=email_data["recipient"],
                subject=email_data["subject"],
                body=email_data["body"],
                timestamp=datetime.utcnow(),
                read=email_data["read"]
            )
            db.add(email)
    db.commit()


# ================================
# Endpoints
# ================================

@app.post("/send", response_model=dict)
def send_email(email: EmailCreate, db: Session = Depends(get_db)):
    """Send a new email."""
    new_email = Email(
        sender=email.sender,
        recipient=email.recipient,
        subject=email.subject,
        body=email.body,
        timestamp=datetime.utcnow(),
        read=False
    )
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    return {"id": new_email.id, "message": "Email sent successfully"}


@app.get("/emails", response_model=List[EmailResponse])
def list_emails(db: Session = Depends(get_db)):
    """List all emails, newest first."""
    emails = db.query(Email).order_by(Email.timestamp.desc()).all()
    return emails


@app.get("/emails/unread", response_model=List[EmailResponse])
def list_unread_emails(db: Session = Depends(get_db)):
    """List only unread emails."""
    emails = db.query(Email).filter(Email.read == False).order_by(Email.timestamp.desc()).all()
    return emails


@app.get("/emails/search", response_model=List[EmailResponse])
def search_emails(q: str = Query(..., description="Search query"), db: Session = Depends(get_db)):
    """Search emails by keyword in subject, body, or sender."""
    emails = db.query(Email).filter(
        (Email.subject.ilike(f"%{q}%")) |
        (Email.body.ilike(f"%{q}%")) |
        (Email.sender.ilike(f"%{q}%"))
    ).order_by(Email.timestamp.desc()).all()
    return emails


@app.get("/emails/filter", response_model=List[EmailResponse])
def filter_emails(
    recipient: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Filter emails by recipient and/or date range."""
    query = db.query(Email)

    if recipient:
        query = query.filter(Email.recipient == recipient)
    if start_date:
        query = query.filter(Email.timestamp >= start_date)
    if end_date:
        query = query.filter(Email.timestamp <= end_date)

    return query.order_by(Email.timestamp.desc()).all()


@app.get("/emails/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    """Fetch a specific email by ID."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@app.patch("/emails/{email_id}/read", response_model=dict)
def mark_email_as_read(email_id: int, db: Session = Depends(get_db)):
    """Mark an email as read."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    email.read = True
    db.commit()
    return {"id": email_id, "message": "Email marked as read"}


@app.patch("/emails/{email_id}/unread", response_model=dict)
def mark_email_as_unread(email_id: int, db: Session = Depends(get_db)):
    """Mark an email as unread."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    email.read = False
    db.commit()
    return {"id": email_id, "message": "Email marked as unread"}


@app.delete("/emails/{email_id}", response_model=dict)
def delete_email(email_id: int, db: Session = Depends(get_db)):
    """Delete an email by ID."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    db.delete(email)
    db.commit()
    return {"id": email_id, "message": "Email deleted successfully"}


@app.get("/reset_database", response_model=dict)
def reset_database(db: Session = Depends(get_db)):
    """Reset emails to initial state (for testing)."""
    # Delete all emails
    db.query(Email).delete()
    db.commit()

    # Re-seed with initial data
    seed_database(db)

    return {"message": "Database reset to initial state"}


# ================================
# Startup Event
# ================================

@app.on_event("startup")
def startup_event():
    """Initialize database with seed data on startup."""
    db = next(get_db())
    seed_database(db)
    db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
