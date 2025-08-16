from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.models import CanteenMenu, User
from app.schemas.canteen import CanteenMenuCreate, CanteenMenuUpdate, CanteenMenu as CanteenMenuSchema
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.get("/{day}", response_model=List[CanteenMenuSchema])
def get_canteen_menu_by_day(day: str, category: Optional[str] = None, db: Session = Depends(get_db)):
    """Fetch menu for a specific day"""
    day = day.capitalize()  # Normalize day format
    query = db.query(CanteenMenu).filter(CanteenMenu.day == day)
    
    if category:
        query = query.filter(CanteenMenu.category == category.lower())
    
    menu_items = query.all()
    return menu_items

@router.get("/", response_model=List[CanteenMenuSchema])
def get_all_canteen_menus(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Fetch all menu items"""
    query = db.query(CanteenMenu)
    
    if category:
        query = query.filter(CanteenMenu.category == category.lower())
    
    menu_items = query.all()
    return menu_items

@router.post("/", response_model=CanteenMenuSchema)
def create_canteen_menu_item(
    menu_item: CanteenMenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Add/update menu items (admin only)"""
    menu_item.day = menu_item.day.capitalize()  # Normalize day format
    if menu_item.category:
        menu_item.category = menu_item.category.lower()  # Normalize category format
    
    # Check if item already exists for the same day and name
    existing_item = db.query(CanteenMenu).filter(
        CanteenMenu.day == menu_item.day,
        CanteenMenu.item == menu_item.item
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu item '{menu_item.item}' already exists for {menu_item.day}"
        )
    
    db_menu_item = CanteenMenu(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.put("/{item_id}", response_model=CanteenMenuSchema)
def update_canteen_menu_item(
    item_id: int,
    menu_item_update: CanteenMenuUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a menu item (admin only)"""
    db_menu_item = db.query(CanteenMenu).filter(CanteenMenu.id == item_id).first()
    if not db_menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    update_data = menu_item_update.dict(exclude_unset=True)
    if "day" in update_data:
        update_data["day"] = update_data["day"].capitalize()
    if "category" in update_data and update_data["category"]:
        update_data["category"] = update_data["category"].lower()
    
    for field, value in update_data.items():
        setattr(db_menu_item, field, value)
    
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@router.delete("/{item_id}")
def delete_canteen_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a menu item (admin only)"""
    db_menu_item = db.query(CanteenMenu).filter(CanteenMenu.id == item_id).first()
    if not db_menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    db.delete(db_menu_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}

@router.get("/categories/list")
def get_available_categories(db: Session = Depends(get_db)):
    """Get list of all available categories"""
    categories = db.query(CanteenMenu.category).distinct().all()
    return {"categories": [category[0] for category in categories if category[0]]}
