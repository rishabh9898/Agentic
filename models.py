# ================================
# Database Models
# ================================

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./emails.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initial seed data
INITIAL_EMAILS = [
    {
        "id": 1,
        "sender": "eric@work.com",
        "recipient": "you@email.com",
        "subject": "Happy Hour",
        "body": "We're planning drinks this Friday!",
        "read": False
    },
    {
        "id": 2,
        "sender": "boss@email.com",
        "recipient": "you@email.com",
        "subject": "Q3 Report Review",
        "body": "Please review the Q3 report and send me your feedback by EOD.",
        "read": False
    },
    {
        "id": 3,
        "sender": "alice@work.com",
        "recipient": "you@email.com",
        "subject": "Lunch Tomorrow?",
        "body": "Hey! Want to grab lunch tomorrow? I was thinking that new Thai place.",
        "read": False
    },
    {
        "id": 4,
        "sender": "newsletter@techdigest.com",
        "recipient": "you@email.com",
        "subject": "Weekly Tech Digest",
        "body": "This week in tech: AI breakthroughs, new gadgets, and more...",
        "read": True
    },
    {
        "id": 5,
        "sender": "boss@email.com",
        "recipient": "you@email.com",
        "subject": "Team Meeting Monday",
        "body": "Reminder: Team meeting at 10 AM Monday. Please prepare your updates.",
        "read": False
    },
    {
        "id": 6,
        "sender": "hr@company.com",
        "recipient": "you@email.com",
        "subject": "Benefits Enrollment Reminder",
        "body": "Open enrollment ends next Friday. Don't forget to update your benefits.",
        "read": True
    }
]
