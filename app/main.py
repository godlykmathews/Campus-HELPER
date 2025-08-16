from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import timetable, bus, canteen, auth
from app.core.database import engine
from app.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Campus Helper API",
    description="A backend service providing useful information for students including class timetables, bus timings, and canteen menus.",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(timetable.router, prefix="/timetable", tags=["Timetable"])
app.include_router(bus.router, prefix="/bus", tags=["Bus"])
app.include_router(canteen.router, prefix="/canteen", tags=["Canteen"])

@app.get("/")
async def root():
    return {"message": "Welcome to Campus Helper API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
