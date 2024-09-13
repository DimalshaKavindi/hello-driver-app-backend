from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.services import optimize_route


router = APIRouter()
@router.get("/optimize_route")
def get_optimized_route() -> Dict[str, Any]:
    optimized_route = optimize_route()
    if optimized_route:
        return {"optimized_route": optimized_route}
    else:
        return {"message": "No solution found"}
