# backend/api/v1/__init__.py

from fastapi import APIRouter
from backend.api.v1.auth import router as auth_router
from backend.api.v1.aqi import router as aqi_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(aqi_router)