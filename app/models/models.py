from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database.database import Base

class Driver(Base):
    __tablename__ = 'drivers'
    
    driver_id = Column(Integer,primary_key=True, index=True)
    driver_name = Column(String, index=True)
    vehicle_capacity = Column(float, index=True)

class Schedule(Base):
    __tablename__ = 'schedules'
    
    schedule_id = Column(Integer, primary_key=True, index=True)
    schedule_driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    status = Column(String, index=True)
    
class Orders(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, index=True)
    longitude = Column(String, index=True)
    latitude = Column(String, index=True)
    order_driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    order_schedule_id = Column(Integer, ForeignKey("schedules.schedule_id"))
    
    

