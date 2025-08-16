from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Timetable(Base):
    __tablename__ = "timetables"
    
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String(20), nullable=False, index=True)  # Monday, Tuesday, etc.
    time = Column(String(20), nullable=False)  # 09:00-10:00
    subject = Column(String(100), nullable=False)
    room = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class BusSchedule(Base):
    __tablename__ = "bus_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    route = Column(String(100), nullable=False, index=True)
    time = Column(String(20), nullable=False)  # 08:30
    bus_no = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class CanteenMenu(Base):
    __tablename__ = "canteen_menus"
    
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String(20), nullable=False, index=True)  # Monday, Tuesday, etc.
    item = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))  # breakfast, lunch, dinner, snacks
    created_at = Column(DateTime, server_default=func.now())
