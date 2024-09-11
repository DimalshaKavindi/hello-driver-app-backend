from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from app.database.database import Base

class Driver(Base):
    __tablename__ = 'drivers'
    
    id = Column(Integer,primary_key=True, index=True)
    driver_id = Column(Integer, index=True)
    driver_name = Column(String, index=True)
    vehicle_capacity = Column(Float, index=True)

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer,primary_key=True, index=True)
    schedule_id = Column(Integer, index=True)
    status = Column(String, index=True)
    schedule_driver_id = Column(Integer, ForeignKey("drivers.id"))
    
class Orders(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer,primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    longitude = Column(String, index=True)
    latitude = Column(String, index=True)
    order_weight = Column(Float, index=True)
    order_driver_id = Column(Integer, ForeignKey("drivers.id"))
    order_schedule_id = Column(Integer, ForeignKey("schedules.id"))
    
    

