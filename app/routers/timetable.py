from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Timetable, User
from app.schemas.timetable import TimetableCreate, TimetableUpdate, Timetable as TimetableSchema
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.get("/{day}", response_model=List[TimetableSchema])
def get_timetable_by_day(day: str, db: Session = Depends(get_db)):
    """Fetch timetable for a specific day"""
    day = day.capitalize()  # Normalize day format
    timetables = db.query(Timetable).filter(Timetable.day == day).all()
    return timetables

@router.get("/", response_model=List[TimetableSchema])
def get_all_timetables(db: Session = Depends(get_db)):
    """Fetch all timetable entries"""
    timetables = db.query(Timetable).all()
    return timetables

@router.post("/", response_model=TimetableSchema)
def create_timetable_entry(
    timetable: TimetableCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Add/update class schedules (admin only)"""
    timetable.day = timetable.day.capitalize()  # Normalize day format
    
    # Check if entry already exists for the same day, time, and room
    existing_entry = db.query(Timetable).filter(
        Timetable.day == timetable.day,
        Timetable.time == timetable.time,
        Timetable.room == timetable.room
    ).first()
    
    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Timetable entry already exists for {timetable.day} at {timetable.time} in room {timetable.room}"
        )
    
    db_timetable = Timetable(**timetable.dict())
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

@router.put("/{timetable_id}", response_model=TimetableSchema)
def update_timetable_entry(
    timetable_id: int,
    timetable_update: TimetableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a timetable entry (admin only)"""
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not db_timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable entry not found"
        )
    
    update_data = timetable_update.dict(exclude_unset=True)
    if "day" in update_data:
        update_data["day"] = update_data["day"].capitalize()
    
    for field, value in update_data.items():
        setattr(db_timetable, field, value)
    
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

@router.delete("/{timetable_id}")
def delete_timetable_entry(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a timetable entry (admin only)"""
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not db_timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable entry not found"
        )
    
    db.delete(db_timetable)
    db.commit()
    return {"message": "Timetable entry deleted successfully"}
