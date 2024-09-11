from fastapi import FastAPI
from app.routes import driver  # Import the driver router

app = FastAPI()

# Include the router for handling driver, schedule, and order-related requests
app.include_router(driver.router, prefix="/api/v1", tags=["drivers"])

# You can add other routers later, e.g., for optimization, etc.
