# backend/repositories/aqi_repository.py

from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from backend.models.aqi_reading import AQIReading


class AQIRepository:
    """
    Handles all database operations for AQI Readings.
    """

    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(self, location_id: UUID, data: dict) -> AQIReading:
        """Saves a new AQI reading to database"""
        pollutants = data.get("pollutants", {})
        weather = data.get("weather", {})

        reading = AQIReading(
            location_id=location_id,
            aqi_value=data.get("aqi_value"),
            aqi_category=data.get("aqi_category"),
            dominant_pollutant=data.get("dominant_pollutant"),
            pm25=pollutants.get("pm25"),
            pm10=pollutants.get("pm10"),
            o3=pollutants.get("o3"),
            no2=pollutants.get("no2"),
            so2=pollutants.get("so2"),
            co=pollutants.get("co"),
            temperature=weather.get("temperature"),
            humidity=weather.get("humidity"),
            wind_speed=weather.get("wind_speed"),
            raw_data=data.get("raw_data"),
            recorded_at=data.get("recorded_at")
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        return reading

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────
    def get_by_id(self, reading_id: UUID) -> Optional[AQIReading]:
        """Finds reading by UUID"""
        return self.db.query(AQIReading).filter(
            AQIReading.id == reading_id
        ).first()

    def get_latest_by_location(self, location_id: UUID) -> Optional[AQIReading]:
        """Returns most recent AQI reading for a location"""
        return self.db.query(AQIReading).filter(
            AQIReading.location_id == location_id
        ).order_by(AQIReading.created_at.desc()).first()

    def get_history_by_location(
        self,
        location_id: UUID,
        limit: int = 24
    ) -> list[AQIReading]:
        """Returns AQI history for a location"""
        return self.db.query(AQIReading).filter(
            AQIReading.location_id == location_id
        ).order_by(AQIReading.created_at.desc()).limit(limit).all()