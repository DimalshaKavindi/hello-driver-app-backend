from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import models
from app.database.database import get_db
from typing import List
from pydantic import BaseModel

router = APIRouter()

class OrderBase(BaseModel):
    order_id: int
    longitude: str
    latitude: str
    order_weight: float

class ScheduleBase(BaseModel):
    schedule_id: int
    status: str
    orders: List[OrderBase]

class DriverBase(BaseModel):
    driver_id: int
    driver_name: str
    vehicle_capacity: float
    schedules: List[ScheduleBase]

@router.post("/drivers/")
async def create_driver(driver: DriverBase, db: Session = Depends(get_db)):
    db_driver = models.Driver(
        driver_id=driver.driver_id, 
        driver_name=driver.driver_name, 
        vehicle_capacity=driver.vehicle_capacity
    )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    
    for schedule in driver.schedules:
        db_schedule = models.Schedule(
            schedule_id=schedule.schedule_id, 
            status=schedule.status, 
            schedule_driver_id=db_driver.id
        )
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        
        for order in schedule.orders:
            db_order = models.Orders(
                order_id=order.order_id,
                longitude=order.longitude,
                latitude=order.latitude, 
                order_weight=order.order_weight,
                order_schedule_id=db_schedule.id,
                order_driver_id=db_driver.id
            )
            db.add(db_order)
        db.commit()

    return {"message": "Driver, schedules, and orders created successfully!"}
