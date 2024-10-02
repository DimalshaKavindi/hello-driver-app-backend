# from pydantic import BaseModel
# from typing import List

# class OrderBase(BaseModel):
#     order_id: int
#     order_weight: float
#     latitude: str
#     longitude: str
#     arrive_time: str

#     class Config:
#         from_attributes = True

# class VehicleRouteBase(BaseModel):
#     vehicle_id: int
#     no_of_orders_for_route: int
#     total_weight_for_route: float
#     total_distance_for_route: float
#     total_time_for_route: float
#     orders: List[OrderBase]

#     class Config:
#         from_attributes = True

# class RoutesBase(BaseModel):
#     no_of_orders: int
#     total_weight: float
#     total_distance: float
#     total_time: float
#     vehicle_routes: List[VehicleRouteBase]

#     class Config:
#         from_attributes = True
