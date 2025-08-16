from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import User, Timetable, BusSchedule, CanteenMenu, Base
from app.core.security import get_password_hash

# Create database tables
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@campus.edu",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin_user)
        
        # Create regular user
        student_user = User(
            username="student",
            email="student@campus.edu",
            hashed_password=get_password_hash("student123"),
            is_admin=False
        )
        db.add(student_user)
        
        # Sample timetable data
        timetable_data = [
            {"day": "Monday", "time": "09:00-10:00", "subject": "Mathematics", "room": "Room 101"},
            {"day": "Monday", "time": "10:00-11:00", "subject": "Physics", "room": "Room 102"},
            {"day": "Monday", "time": "11:00-12:00", "subject": "Chemistry", "room": "Room 103"},
            {"day": "Tuesday", "time": "09:00-10:00", "subject": "English", "room": "Room 201"},
            {"day": "Tuesday", "time": "10:00-11:00", "subject": "History", "room": "Room 202"},
            {"day": "Wednesday", "time": "09:00-10:00", "subject": "Computer Science", "room": "Lab 1"},
            {"day": "Wednesday", "time": "10:00-11:00", "subject": "Biology", "room": "Room 301"},
            {"day": "Thursday", "time": "09:00-10:00", "subject": "Geography", "room": "Room 401"},
            {"day": "Friday", "time": "09:00-10:00", "subject": "Art", "room": "Room 501"},
        ]
        
        for item in timetable_data:
            timetable = Timetable(**item)
            db.add(timetable)
        
        # Sample bus schedule data
        bus_data = [
            {"route": "Main Gate to Engineering Block", "time": "08:00", "bus_no": "BUS-001"},
            {"route": "Main Gate to Engineering Block", "time": "09:00", "bus_no": "BUS-002"},
            {"route": "Main Gate to Engineering Block", "time": "10:00", "bus_no": "BUS-001"},
            {"route": "Engineering Block to Main Gate", "time": "16:00", "bus_no": "BUS-001"},
            {"route": "Engineering Block to Main Gate", "time": "17:00", "bus_no": "BUS-002"},
            {"route": "Hostel to Academic Block", "time": "08:30", "bus_no": "BUS-003"},
            {"route": "Hostel to Academic Block", "time": "09:30", "bus_no": "BUS-004"},
            {"route": "Academic Block to Hostel", "time": "16:30", "bus_no": "BUS-003"},
        ]
        
        for item in bus_data:
            bus_schedule = BusSchedule(**item)
            db.add(bus_schedule)
        
        # Sample canteen menu data
        menu_data = [
            {"day": "Monday", "item": "Chicken Curry", "price": 120.0, "category": "lunch"},
            {"day": "Monday", "item": "Rice", "price": 40.0, "category": "lunch"},
            {"day": "Monday", "item": "Dal", "price": 60.0, "category": "lunch"},
            {"day": "Monday", "item": "Chapati", "price": 20.0, "category": "lunch"},
            {"day": "Monday", "item": "Tea", "price": 15.0, "category": "breakfast"},
            {"day": "Monday", "item": "Sandwich", "price": 80.0, "category": "breakfast"},
            {"day": "Tuesday", "item": "Fish Fry", "price": 150.0, "category": "lunch"},
            {"day": "Tuesday", "item": "Rice", "price": 40.0, "category": "lunch"},
            {"day": "Tuesday", "item": "Coffee", "price": 20.0, "category": "breakfast"},
            {"day": "Wednesday", "item": "Vegetable Biryani", "price": 100.0, "category": "lunch"},
            {"day": "Wednesday", "item": "Raita", "price": 30.0, "category": "lunch"},
            {"day": "Thursday", "item": "Mutton Curry", "price": 180.0, "category": "lunch"},
            {"day": "Friday", "item": "Chicken Biryani", "price": 140.0, "category": "lunch"},
        ]
        
        for item in menu_data:
            menu = CanteenMenu(**item)
            db.add(menu)
        
        db.commit()
        print("Sample data created successfully!")
        print("Admin credentials: username='admin', password='admin123'")
        print("Student credentials: username='student', password='student123'")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
