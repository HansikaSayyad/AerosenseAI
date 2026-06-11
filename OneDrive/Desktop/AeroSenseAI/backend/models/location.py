# backend/models/location.py

from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.connection import Base
import uuid


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # ─────────────────────────────────────────
    # FOREIGN KEY — links to users table
    # ─────────────────────────────────────────
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # ─────────────────────────────────────────
    # LOCATION FIELDS
    # Supports both city and GPS
    # ─────────────────────────────────────────
    name = Column(String, nullable=False)           # "Home", "Office"
    city = Column(String, nullable=True)            # "Vijayawada"
    country = Column(String, nullable=True)         # "India"
    latitude = Column(Float, nullable=True)         # 16.5062
    longitude = Column(Float, nullable=True)        # 80.6480
    is_default = Column(Boolean, default=False)     # primary location

    # ─────────────────────────────────────────
    # TIMESTAMPS
    # ─────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ─────────────────────────────────────────
    # RELATIONSHIPS
    # ─────────────────────────────────────────
    user = relationship("User", back_populates="locations")
    aqi_readings = relationship("AQIReading", back_populates="location", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Location {self.name} - {self.city}>"