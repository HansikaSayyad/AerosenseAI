# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.core.config import settings
from backend.database.connection import Base, engine, test_connection


# ─────────────────────────────────────────
# LIFESPAN — runs on startup and shutdown
# ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: create tables, test DB connection
    Shutdown: cleanup
    """
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Test database connection
    test_connection()

    # Create all tables automatically
    import backend.models  # noqa — ensures models are registered
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

    yield  # App runs here

    print(f"👋 Shutting down {settings.APP_NAME}")


# ─────────────────────────────────────────
# CREATE FASTAPI APP
# ─────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic Air Quality Monitoring and Recommendation Platform",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
    lifespan=lifespan
)


# ─────────────────────────────────────────
# CORS MIDDLEWARE
# Allows React frontend to call our API
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
# REGISTER ALL ROUTES
# ─────────────────────────────────────────
from backend.api.v1 import api_router
app.include_router(api_router)


# ─────────────────────────────────────────
# HEALTH CHECK ROUTE
# ─────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "app": settings.APP_NAME
    }


# ─────────────────────────────────────────
# QUICK AQI TEST ROUTE
# Tests all 3 agents together
# ─────────────────────────────────────────
@app.get("/test-agents", tags=["Test"])
async def test_agents(city: str = "Hyderabad"):
    """
    Test all 3 agents pipeline:
    DataCollection → Analysis → Recommendation
    """
    from backend.agents import (
        DataCollectionAgent,
        AnalysisAgent,
        RecommendationAgent
    )

    # Run agent pipeline
    collector   = DataCollectionAgent()
    analyzer    = AnalysisAgent()
    recommender = RecommendationAgent()

    result1 = collector.run({"city": city})
    if not result1.success:
        return {"error": result1.error}

    result2 = analyzer.run(result1.data)
    if not result2.success:
        return {"error": result2.error}

    result3 = recommender.run(result2.data)
    if not result3.success:
        return {"error": result3.error}

    return {
        "success": True,
        "city": city,
        "aqi_value": result3.data.get("aqi_value"),
        "aqi_category": result3.data.get("aqi_category"),
        "recommendations": result3.data.get("recommendations")
    }