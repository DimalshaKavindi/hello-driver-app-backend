from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.services import create_data, create_distance_matrix, solve_vrp

router = APIRouter()

@router.get("/distance_matrix", response_model=List[List[int]])
async def get_distance_matrix():
    try:
        data = create_data()
        distance_matrix = create_distance_matrix(data)
        return distance_matrix
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building distance matrix: {e}")
    
@router.get("/solve_vrp")
async def solve_vrp_endpoint():
    try:
        solve_vrp()
        return {"message": "VRP solution calculated and printed in the console."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving VRP: {e}")