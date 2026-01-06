from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.controllers.inventory import router as inventory_router
from app.controllers.checkout import router as checkout_router


load_dotenv()

app = FastAPI(
    title="FlexyPe Smart Inventory Reservation System",
    description="Backend system with TTL reservations, fairness engine, waitlist, and AI insights",
    version="1.0.0"
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FlexyPe Smart Inventory Reservation System is running",
        "docs": "/docs",
        "health": "/health"
    }
app.include_router(inventory_router)
app.include_router(checkout_router)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
