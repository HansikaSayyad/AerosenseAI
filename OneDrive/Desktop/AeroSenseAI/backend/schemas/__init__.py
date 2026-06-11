# backend/schemas/__init__.py

from backend.schemas.user import (
    UserBase,
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    Token,
    TokenData
)
from backend.schemas.aqi import (
    AQIByCity,
    AQIByGPS,
    AQIResponse,
    PollutantData,
    LocationCreate,
    LocationResponse
)
from backend.schemas.recommendation import (
    RecommendationResponse,
    SuccessResponse,
    ErrorResponse
)