from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.vrp_routes_model import models
from app.database.vrp_routes_db import get_db
from typing import List
from pydantic import BaseModel

# Create the API Router
router = APIRouter()

# Pydantic models for request and response schemas
class OrderBase(BaseModel):
    order_id: int
    order_weight: float
    latitude: str
    longitude: str
    arrive_time: str

class RouteDetailBase(BaseModel):
    no_of_orders_for_route: int
    total_weight_for_route: float
    total_distance_for_route: float
    total_time_for_route: int
    vehicle_id: int
    orders: List[OrderBase]

class RouteBase(BaseModel):
    no_of_orders: int
    total_weight: float
    total_distance: float
    total_time: int
    route: List[RouteDetailBase]

# # Endpoint to create a new route
# @router.post("/routes/", response_model=RouteBase)
# def create_route(route_data: RouteBase, db: Session = Depends(get_db)):
#     # Create Route
#     route = models.Route(
#         no_of_orders=route_data.no_of_orders,
#         total_weight=route_data.total_weight,
#         total_distance=route_data.total_distance,
#         total_time=route_data.total_time
#     )
#     db.add(route)
#     db.commit()
#     db.refresh(route)

#     # Create RouteDetails and Orders
#     for detail_data in route_data.route:
#         route_detail = models.RouteDetail(
#             no_of_orders_for_route=detail_data.no_of_orders_for_route,
#             total_weight_for_route=detail_data.total_weight_for_route,
#             total_distance_for_route=detail_data.total_distance_for_route,
#             total_time_for_route=detail_data.total_time_for_route,
#             vehicle_id=detail_data.vehicle_id,
#             route_id=route.id
#         )
#         db.add(route_detail)
#         db.commit()
#         db.refresh(route_detail)

#         # Add orders for each route detail
#         for order_data in detail_data.orders:
#             order = models.Order(
#                 order_id=order_data.order_id,
#                 order_weight=order_data.order_weight,
#                 latitude=order_data.latitude,
#                 longitude=order_data.longitude,
#                 arrive_time=order_data.arrive_time,
#                 route_detail_id=route_detail.id
#             )
#             db.add(order)
#             db.commit()
#             db.refresh(order)

#     return route_data

# # Endpoint to retrieve a route by ID
# @router.get("/routes/{route_id}", response_model=RouteBase)
# def get_route(route_id: int, db: Session = Depends(get_db)):
#     route = db.query(models.Route).filter(models.Route.id == route_id).first()
#     if not route:
#         raise HTTPException(status_code=404, detail="Route not found")

#     # Fetch Route Details and Orders
#     route_details = db.query(models.RouteDetail).filter(models.RouteDetail.route_id == route_id).all()
#     result_details = []
    
#     for detail in route_details:
#         orders = db.query(models.Order).filter(models.Order.route_detail_id == detail.id).all()
#         result_orders = [OrderBase(**order.__dict__) for order in orders]
#         detail_data = RouteDetailBase(
#             no_of_orders_for_route=detail.no_of_orders_for_route,
#             total_weight_for_route=detail.total_weight_for_route,
#             total_distance_for_route=detail.total_distance_for_route,
#             total_time_for_route=detail.total_time_for_route,
#             vehicle_id=detail.vehicle_id,
#             orders=result_orders
#         )
#         result_details.append(detail_data)

#     route_data = RouteBase(
#         no_of_orders=route.no_of_orders,
#         total_weight=route.total_weight,
#         total_distance=route.total_distance,
#         total_time=route.total_time,
#         route=result_details
#     )

#     return route_data

# # Endpoint to list all routes
# @router.get("/routes/", response_model=List[RouteBase])
# def list_routes(db: Session = Depends(get_db)):
#     routes = db.query(models.Route).all()
#     all_routes = []

#     for route in routes:
#         # Fetch Route Details and Orders
#         route_details = db.query(models.RouteDetail).filter(models.RouteDetail.route_id == route.id).all()
#         result_details = []

#         for detail in route_details:
#             orders = db.query(models.Order).filter(models.Order.route_detail_id == detail.id).all()
#             result_orders = [OrderBase(**order.__dict__) for order in orders]
#             detail_data = RouteDetailBase(
#                 no_of_orders_for_route=detail.no_of_orders_for_route,
#                 total_weight_for_route=detail.total_weight_for_route,
#                 total_distance_for_route=detail.total_distance_for_route,
#                 total_time_for_route=detail.total_time_for_route,
#                 vehicle_id=detail.vehicle_id,
#                 orders=result_orders
#             )
#             result_details.append(detail_data)

#         route_data = RouteBase(
#             no_of_orders=route.no_of_orders,
#             total_weight=route.total_weight,
#             total_distance=route.total_distance,
#             total_time=route.total_time,
#             route=result_details
#         )

#         all_routes.append(route_data)

#     return all_routes
