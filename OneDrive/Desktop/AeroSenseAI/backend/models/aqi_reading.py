# backend/models/aqi_reading.py

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.connection import Base
import uuid


class AQIReading(Base):
    __tablename__ = "aqi_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # ─────────────────────────────────────────
    # FOREIGN KEY
    # ─────────────────────────────────────────
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)

    # ─────────────────────────────────────────
    # AQI DATA
    # ─────────────────────────────────────────
    aqi_value = Column(Integer, nullable=True)
    aqi_category = Column(String, nullable=True)  # Good, Moderate, Unhealthy etc
    dominant_pollutant = Column(String, nullable=True)  # pm25, pm10, o3 etc

    # ─────────────────────────────────────────
    # INDIVIDUAL POLLUTANTS
    # ─────────────────────────────────────────
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    so2 = Column(Float, nullable=True)
    co = Column(Float, nullable=True)

    # ─────────────────────────────────────────
    # WEATHER DATA
    # ─────────────────────────────────────────
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)

    # ─────────────────────────────────────────
    # RAW API RESPONSE
    # Stored as JSON for future use
    # ─────────────────────────────────────────
    raw_data = Column(JSON, nullable=True)

    # ─────────────────────────────────────────
    # TIMESTAMPS
    # ─────────────────────────────────────────
    recorded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ─────────────────────────────────────────
    # RELATIONSHIPS
    # ─────────────────────────────────────────
    location = relationship("Location", back_populates="aqi_readings")
    recommendations = relationship("Recommendation", back_populates="aqi_reading")

    def __repr__(self):
        return f"<AQIReading AQI={self.aqi_value} Category={self.aqi_category}>"