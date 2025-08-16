from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusScheduleBase(BaseModel):
    route: str
    time: str
    bus_no: str

class BusScheduleCreate(BusScheduleBase):
    pass

class BusScheduleUpdate(BaseModel):
    route: Optional[str] = None
    time: Optional[str] = None
    bus_no: Optional[str] = None

class BusSchedule(BusScheduleBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
