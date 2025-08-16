from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CanteenMenuBase(BaseModel):
    day: str
    item: str
    price: float
    category: Optional[str] = None

class CanteenMenuCreate(CanteenMenuBase):
    pass

class CanteenMenuUpdate(BaseModel):
    day: Optional[str] = None
    item: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class CanteenMenu(CanteenMenuBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True  # Changed from from_attributes to orm_mode
