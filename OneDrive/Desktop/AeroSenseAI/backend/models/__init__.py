# backend/models/__init__.py
# Import all models so SQLAlchemy knows about them

from backend.models.user import User, UserRole
from backend.models.location import Location
from backend.models.aqi_reading import AQIReading
from backend.models.recommendation import Recommendation