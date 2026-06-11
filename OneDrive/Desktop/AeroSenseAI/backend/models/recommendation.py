# backend/models/recommendation.py

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.connection import Base
import uuid


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # ─────────────────────────────────────────
    # FOREIGN KEYS
    # ─────────────────────────────────────────
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    aqi_reading_id = Column(UUID(as_uuid=True), ForeignKey("aqi_readings.id"), nullable=True)

    # ─────────────────────────────────────────
    # RECOMMENDATION DATA
    # ─────────────────────────────────────────
    aqi_category = Column(String, nullable=False)
    general_advice = Column(Text, nullable=True)
    outdoor_activity = Column(String, nullable=True)   # safe, limited, avoid
    mask_required = Column(String, nullable=True)      # yes, no, optional
    window_advice = Column(String, nullable=True)      # open, closed

    # ─────────────────────────────────────────
    # SENSITIVE GROUPS ADVICE
    # Stored as JSON list
    # ─────────────────────────────────────────
    sensitive_groups = Column(JSON, nullable=True)

    # ─────────────────────────────────────────
    # TIMESTAMPS
    # ─────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ─────────────────────────────────────────
    # RELATIONSHIPS
    # ─────────────────────────────────────────
    user = relationship("User", back_populates="recommendations")
    aqi_reading = relationship("AQIReading", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation {self.aqi_category}>"