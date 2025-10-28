from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Perform startup tasks if needed
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Perform shutdown tasks if needed
    pass

app.include_router(api_router, prefix="/api/v1")