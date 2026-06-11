# backend/schemas/aqi.py

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


# ─────────────────────────────────────────
# REQUEST SCHEMAS
# Supports both GPS and City search
# ─────────────────────────────────────────
class AQIByCity(BaseModel):
    """Request schema for city-based AQI lookup"""
    city: str

    @field_validator("city")
    @classmethod
    def validate_city(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("City name must be at least 2 characters")
        return v.strip()


class AQIByGPS(BaseModel):
    """Request schema for GPS-based AQI lookup"""
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v


# ─────────────────────────────────────────
# POLLUTANT DATA SCHEMA
# ─────────────────────────────────────────
class PollutantData(BaseModel):
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    o3: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None


# ─────────────────────────────────────────
# AQI RESPONSE SCHEMA
# Returned to frontend
# ─────────────────────────────────────────
class AQIResponse(BaseModel):
    city: str
    aqi_value: Optional[int] = None
    aqi_category: Optional[str] = None
    dominant_pollutant: Optional[str] = None
    pollutants: Optional[PollutantData] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    recorded_at: Optional[datetime] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# LOCATION SCHEMAS
# ─────────────────────────────────────────
class LocationCreate(BaseModel):
    name: str
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False


class LocationResponse(LocationCreate):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True