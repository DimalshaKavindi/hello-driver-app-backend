from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.vrp_routes_db import Base

# Route model
class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    no_of_orders = Column(Integer, nullable=False)
    total_weight = Column(Float, nullable=False)
    total_distance = Column(Float, nullable=False)
    total_time = Column(Integer, nullable=False)

    # One-to-many relationship with RouteDetails
    route_details = relationship("RouteDetail", back_populates="route", cascade="all, delete-orphan")


# Route detail model (stores vehicle info and orders in a route)
class RouteDetail(Base):
    __tablename__ = "route_details"
    
    id = Column(Integer, primary_key=True, index=True)
    no_of_orders_for_route = Column(Integer, nullable=False)
    total_weight_for_route = Column(Float, nullable=False)
    total_distance_for_route = Column(Float, nullable=False)
    total_time_for_route = Column(Integer, nullable=False)
    vehicle_id = Column(Integer, nullable=False)
    
    # ForeignKey to link to Route
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"))
    
    # One-to-many relationship with Orders
    orders = relationship("Order", back_populates="route_detail", cascade="all, delete-orphan")
    
    # Back-reference to Route
    route = relationship("Route", back_populates="route_details")


# Order model (stores details of each order)
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    order_weight = Column(Float, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    arrive_time = Column(String, nullable=False)
    
    # ForeignKey to link to RouteDetail
    route_detail_id = Column(Integer, ForeignKey("route_details.id", ondelete="CASCADE"))
    
    # Back-reference to RouteDetail
    route_detail = relationship("RouteDetail", back_populates="orders")
