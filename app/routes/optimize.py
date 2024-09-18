from fastapi import APIRouter, HTTPException
from typing import List
from app.services.services import solve_vrp, create_data, create_matrix

router = APIRouter()

@router.get("/distance_matrix")
async def get_distance_matrix():
    try:
        data = create_data()
        time_windows = data["time_windows"]
        distance_matrix, time_matrix = create_matrix(data)
        return {"distance_matrix": distance_matrix, "time_matrix": time_matrix, "time_windows" : time_windows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building distance matrix: {e}")


@router.get("/solve_vrp")
async def solve_vrp_endpoint():
    try:
        solve_vrp()
        return {"message": "VRP solution calculated and printed in the console."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving VRP: {e}")