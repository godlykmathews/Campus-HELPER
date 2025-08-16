from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import BusSchedule, User
from app.schemas.bus import BusScheduleCreate, BusScheduleUpdate, BusSchedule as BusScheduleSchema
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.get("/{route}", response_model=List[BusScheduleSchema])
def get_bus_timings_by_route(route: str, db: Session = Depends(get_db)):
    """Fetch bus timings for a given route"""
    bus_schedules = db.query(BusSchedule).filter(BusSchedule.route.ilike(f"%{route}%")).all()
    if not bus_schedules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bus schedules found for route: {route}"
        )
    return bus_schedules

@router.get("/", response_model=List[BusScheduleSchema])
def get_all_bus_schedules(db: Session = Depends(get_db)):
    """Fetch all available routes with timings"""
    bus_schedules = db.query(BusSchedule).all()
    return bus_schedules

@router.post("/", response_model=BusScheduleSchema)
def create_bus_schedule(
    bus_schedule: BusScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Add/update bus schedules (admin only)"""
    # Check if schedule already exists for the same route, time, and bus
    existing_schedule = db.query(BusSchedule).filter(
        BusSchedule.route == bus_schedule.route,
        BusSchedule.time == bus_schedule.time,
        BusSchedule.bus_no == bus_schedule.bus_no
    ).first()
    
    if existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bus schedule already exists for route {bus_schedule.route} at {bus_schedule.time}"
        )
    
    db_bus_schedule = BusSchedule(**bus_schedule.dict())
    db.add(db_bus_schedule)
    db.commit()
    db.refresh(db_bus_schedule)
    return db_bus_schedule

@router.put("/{schedule_id}", response_model=BusScheduleSchema)
def update_bus_schedule(
    schedule_id: int,
    bus_schedule_update: BusScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a bus schedule (admin only)"""
    db_bus_schedule = db.query(BusSchedule).filter(BusSchedule.id == schedule_id).first()
    if not db_bus_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus schedule not found"
        )
    
    update_data = bus_schedule_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bus_schedule, field, value)
    
    db.commit()
    db.refresh(db_bus_schedule)
    return db_bus_schedule

@router.delete("/{schedule_id}")
def delete_bus_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a bus schedule (admin only)"""
    db_bus_schedule = db.query(BusSchedule).filter(BusSchedule.id == schedule_id).first()
    if not db_bus_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus schedule not found"
        )
    
    db.delete(db_bus_schedule)
    db.commit()
    return {"message": "Bus schedule deleted successfully"}

@router.get("/routes/list")
def get_available_routes(db: Session = Depends(get_db)):
    """Get list of all available routes"""
    routes = db.query(BusSchedule.route).distinct().all()
    return {"routes": [route[0] for route in routes]}
