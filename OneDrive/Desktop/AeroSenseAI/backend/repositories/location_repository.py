# backend/repositories/location_repository.py

from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from backend.models.location import Location


class LocationRepository:
    """
    Handles all database operations for Locations.
    """

    def __init__(self, db: Session):
        self.db = db

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(
        self,
        user_id: UUID,
        name: str,
        city: Optional[str] = None,
        country: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        is_default: bool = False
    ) -> Location:
        """Creates a new location for a user"""
        # If this is default, unset other defaults first
        if is_default:
            self._unset_defaults(user_id)

        location = Location(
            user_id=user_id,
            name=name,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            is_default=is_default
        )
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────
    def get_by_id(self, location_id: UUID) -> Optional[Location]:
        """Finds location by UUID"""
        return self.db.query(Location).filter(
            Location.id == location_id
        ).first()

    def get_user_locations(self, user_id: UUID) -> list[Location]:
        """Returns all locations for a user"""
        return self.db.query(Location).filter(
            Location.user_id == user_id
        ).all()

    def get_default_location(self, user_id: UUID) -> Optional[Location]:
        """Returns user's default location"""
        return self.db.query(Location).filter(
            Location.user_id == user_id,
            Location.is_default == True
        ).first()

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, location_id: UUID) -> bool:
        """Deletes a location"""
        location = self.get_by_id(location_id)
        if not location:
            return False
        self.db.delete(location)
        self.db.commit()
        return True

    # ─────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────
    def _unset_defaults(self, user_id: UUID) -> None:
        """Removes default flag from all user locations"""
        self.db.query(Location).filter(
            Location.user_id == user_id,
            Location.is_default == True
        ).update({"is_default": False})
        self.db.commit()