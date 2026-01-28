# ================================
# Pydantic Schemas
# ================================

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class EmailCreate(BaseModel):
    recipient: str
    subject: str
    body: str
    sender: Optional[str] = "you@email.com"


class EmailResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: datetime
    read: bool

    class Config:
        from_attributes = True


class EmailFilter(BaseModel):
    recipient: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
