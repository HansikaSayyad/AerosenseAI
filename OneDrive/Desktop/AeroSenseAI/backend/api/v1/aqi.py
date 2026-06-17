# backend/api/v1/aqi.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from backend.database.connection import get_db
from backend.schemas.aqi import AQIByGPS
from backend.security.rbac import rbac

router = APIRouter(prefix="/aqi", tags=["Air Quality"])


# ─────────────────────────────────────────
# GET AQI BY CITY — Public
# ─────────────────────────────────────────
@router.get("/city", response_model=dict)
async def get_aqi_by_city(
    city: str = Query(..., description="City name e.g. Hyderabad"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(rbac.optional_auth),
):
    """
    Get real-time AQI data for a city.
    Saves reading to history when user is logged in.
    """
    from backend.agents.data_collection_agent import DataCollectionAgent
    from backend.agents.analysis_agent import AnalysisAgent
    from backend.agents.recommendation_agent import RecommendationAgent

    collector   = DataCollectionAgent()
    analyzer    = AnalysisAgent()
    recommender = RecommendationAgent()

    r1 = collector.run({"city": city})
    if not r1.success:
        return {"success": False, "error": r1.error}

    r2 = analyzer.run(r1.data)
    r3 = recommender.run(r2.data)
    data = r3.data

    # Save to DB if user is authenticated
    if current_user:
        try:
            from backend.services.aqi_service import AQIService
            svc = AQIService(db)
            svc.save_aqi_reading(
                user_id=UUID(current_user["sub"]),
                location_data={"city": data.get("city")},
                aqi_data=data
            )
        except Exception:
            pass  # Never block the response due to DB write failure

    return {
        "success": True,
        "city": data.get("city"),
        "aqi_value": data.get("aqi_value"),
        "aqi_category": data.get("aqi_category"),
        "aqi_color": data.get("aqi_color"),
        "dominant_pollutant": data.get("dominant_pollutant"),
        "health_risk_level": data.get("health_risk_level"),
        "pollutants": data.get("pollutants"),
        "weather": data.get("weather"),
        "recommendations": data.get("recommendations"),
        "recorded_at": data.get("recorded_at"),
    }


# ─────────────────────────────────────────
# GET AQI BY GPS — Public
# ─────────────────────────────────────────
@router.post("/gps", response_model=dict)
async def get_aqi_by_gps(
    location: AQIByGPS,
    db: Session = Depends(get_db),
    current_user: dict = Depends(rbac.optional_auth),
):
    """
    Get real-time AQI data by GPS coordinates.
    Saves reading to history when user is logged in.
    """
    from backend.agents.data_collection_agent import DataCollectionAgent
    from backend.agents.analysis_agent import AnalysisAgent
    from backend.agents.recommendation_agent import RecommendationAgent

    collector   = DataCollectionAgent()
    analyzer    = AnalysisAgent()
    recommender = RecommendationAgent()

    r1 = collector.run({
        "latitude": location.latitude,
        "longitude": location.longitude,
    })
    if not r1.success:
        return {"success": False, "error": r1.error}

    r2 = analyzer.run(r1.data)
    r3 = recommender.run(r2.data)
    data = r3.data

    # Save to DB if user is authenticated
    if current_user:
        try:
            from backend.services.aqi_service import AQIService
            svc = AQIService(db)
            svc.save_aqi_reading(
                user_id=UUID(current_user["sub"]),
                location_data={
                    "city": data.get("city"),
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                },
                aqi_data=data
            )
        except Exception:
            pass

    return {
        "success": True,
        "city": data.get("city"),
        "aqi_value": data.get("aqi_value"),
        "aqi_category": data.get("aqi_category"),
        "aqi_color": data.get("aqi_color"),
        "dominant_pollutant": data.get("dominant_pollutant"),
        "health_risk_level": data.get("health_risk_level"),
        "pollutants": data.get("pollutants"),
        "weather": data.get("weather"),
        "recommendations": data.get("recommendations"),
        "recorded_at": data.get("recorded_at"),
    }


# ─────────────────────────────────────────
# GET AQI HISTORY — Protected
# ─────────────────────────────────────────
@router.get("/history", response_model=dict)
async def get_aqi_history(
    limit: int = Query(default=20, le=100),
    current_user: dict = Depends(rbac.require_auth),
    db: Session = Depends(get_db),
):
    """
    Returns the authenticated user's AQI search history,
    sorted newest-first across all their saved locations.
    """
    from backend.repositories.location_repository import LocationRepository
    from backend.repositories.aqi_repository import AQIRepository

    user_id = UUID(current_user["sub"])
    location_repo = LocationRepository(db)
    aqi_repo      = AQIRepository(db)

    locations = location_repo.get_user_locations(user_id)
    if not locations:
        return {"success": True, "history": []}

    history = []
    for loc in locations:
        readings = aqi_repo.get_history_by_location(loc.id, limit=limit)
        for r in readings:
            history.append({
                "id": str(r.id),
                "city": loc.city or loc.name,
                "aqi_value": r.aqi_value,
                "aqi_category": r.aqi_category,
                "dominant_pollutant": r.dominant_pollutant,
                "recorded_at": r.recorded_at.isoformat() if r.recorded_at else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            })

    # Sort newest first and cap at limit
    history.sort(key=lambda x: x["created_at"] or "", reverse=True)
    return {"success": True, "history": history[:limit]}
