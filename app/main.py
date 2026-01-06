from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Controllers
from app.controllers.inventory import router as inventory_router
from app.controllers.checkout import router as checkout_router
from app.controllers.analytics import router as analytics_router

load_dotenv()

# ✅ Create FastAPI app FIRST
app = FastAPI(
    title="FlexyPe Smart Inventory Reservation System",
    description="Concurrency-safe inventory, reservations, waitlists, and analytics",
    version="1.0.0"
)

# ✅ Then include routers
app.include_router(inventory_router)
app.include_router(checkout_router)
app.include_router(analytics_router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FlexyPe Smart Inventory Reservation System is running",
        "docs": "/docs"
    }

# Static frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
