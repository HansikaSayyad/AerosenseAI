# backend/services/aqi_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from backend.agents.data_collection_agent import DataCollectionAgent
from backend.agents.analysis_agent import AnalysisAgent
from backend.agents.recommendation_agent import RecommendationAgent
from backend.repositories.location_repository import LocationRepository
from backend.repositories.aqi_repository import AQIRepository


class AQIService:
    """
    Orchestrates the full AQI pipeline:
    DataCollection → Analysis → Recommendation → Save to DB
    """

    def __init__(self, db: Session):
        self.db = db
        self.location_repo = LocationRepository(db)
        self.aqi_repo = AQIRepository(db)

        # Initialize agents
        self.collector = DataCollectionAgent()
        self.analyzer = AnalysisAgent()
        self.recommender = RecommendationAgent()

    # ─────────────────────────────────────────
    # GET AQI BY CITY
    # ─────────────────────────────────────────
    def get_aqi_by_city(self, city: str) -> dict:
        """
        Full pipeline for city-based AQI:
        1. Collect data from API
        2. Analyze AQI
        3. Generate recommendations
        """
        return self._run_pipeline({"city": city})

    # ─────────────────────────────────────────
    # GET AQI BY GPS
    # ─────────────────────────────────────────
    def get_aqi_by_gps(self, latitude: float, longitude: float) -> dict:
        """
        Full pipeline for GPS-based AQI:
        1. Collect data from API
        2. Analyze AQI
        3. Generate recommendations
        """
        return self._run_pipeline({
            "latitude": latitude,
            "longitude": longitude
        })

    # ─────────────────────────────────────────
    # SAVE AQI READING
    # ─────────────────────────────────────────
    def save_aqi_reading(
        self,
        user_id: UUID,
        location_data: dict,
        aqi_data: dict
    ) -> dict:
        """
        Saves AQI reading to database for a user location.
        Creates location if it doesn't exist.
        """
        # Get or create location
        locations = self.location_repo.get_user_locations(user_id)
        city = aqi_data.get("city", "Unknown")

        location = next(
            (l for l in locations if l.city == city),
            None
        )

        if not location:
            location = self.location_repo.create(
                user_id=user_id,
                name=city,
                city=city,
                latitude=aqi_data.get("latitude"),
                longitude=aqi_data.get("longitude"),
                is_default=len(locations) == 0
            )

        # Save AQI reading
        reading = self.aqi_repo.create(
            location_id=location.id,
            data=aqi_data
        )

        return {
            "location": location,
            "reading": reading
        }

    # ─────────────────────────────────────────
    # GET AQI HISTORY
    # ─────────────────────────────────────────
    def get_aqi_history(self, location_id: UUID, limit: int = 24) -> list:
        """Returns AQI history for a location"""
        return self.aqi_repo.get_history_by_location(location_id, limit)

    # ─────────────────────────────────────────
    # PRIVATE — RUN FULL PIPELINE
    # ─────