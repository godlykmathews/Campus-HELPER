from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimetableBase(BaseModel):
    day: str
    time: str
    subject: str
    room: str

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(BaseModel):
    day: Optional[str] = None
    time: Optional[str] = None
    subject: Optional[str] = None
    room: Optional[str] = None

class Timetable(TimetableBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
