# backend/agents/data_collection_agent.py

import requests
from datetime import datetime
from typing import Optional
from backend.agents.base_agent import BaseAgent, AgentResult
from backend.core.config import settings


class DataCollectionAgent(BaseAgent):
    """
    Responsible for:
    - Fetching AQI data from WAQI API
    - Supporting both city and GPS inputs
    - Normalizing raw API responses
    - Handling API errors gracefully
    """

    def __init__(self):
        super().__init__(name="DataCollectionAgent")
        self.api_key = settings.AQI_API_KEY
        self.base_url = settings.AQI_BASE_URL

    def run(self, input_data: dict) -> AgentResult:
        """
        Main entry point.

        Accepts:
            {"city": "Vijayawada"}
            {"latitude": 16.5062, "longitude": 80.6480}

        Returns:
            AgentResult with normalized AQI data
        """
        start_time = datetime.now()

        try:
            # ─────────────────────────────────────────
            # DECIDE: City or GPS?
            # ─────────────────────────────────────────
            if "city" in input_data:
                raw_data = self._fetch_by_city(input_data["city"])
            elif "latitude" in input_data and "longitude" in input_data:
                raw_data = self._fetch_by_gps(
                    input_data["latitude"],
                    input_data["longitude"]
                )
            else:
                return self.error_result(
                    "Input must contain 'city' or 'latitude' and 'longitude'",
                    self._track_time(start_time)
                )

            # ─────────────────────────────────────────
            # CHECK API RESPONSE
            # ─────────────────────────────────────────
            if raw_data.get("status") != "ok":
                return self.error_result(
                    f"API returned error: {raw_data.get('data', 'Unknown error')}",
                    self._track_time(start_time)
                )

            # ─────────────────────────────────────────
            # NORMALIZE THE DATA
            # ─────────────────────────────────────────
            normalized = self._normalize(raw_data["data"])

            return self.success_result(
                data=normalized,
                execution_time_ms=self._track_time(start_time)
            )

        except requests.exceptions.ConnectionError:
            return self.error_result(
                "Cannot connect to AQI API. Check internet connection.",
                self._track_time(start_time)
            )
        except requests.exceptions.Timeout:
            return self.error_result(
                "AQI API request timed out.",
                self._track_time(start_time)
            )
        except Exception as e:
            return self.error_result(
                f"Unexpected error: {str(e)}",
                self._track_time(start_time)
            )

    def _fetch_by_city(self, city: str) -> dict:
        """Fetch AQI data by city name"""
        url = f"{self.base_url}/feed/{city}/?token={self.api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _fetch_by_gps(self, latitude: float, longitude: float) -> dict:
        """Fetch AQI data by GPS coordinates"""
        url = f"{self.base_url}/feed/geo:{latitude};{longitude}/?token={self.api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _normalize(self, raw: dict) -> dict:
        """
        Converts raw WAQI API response into
        clean standardized format.
        """
        iaqi = raw.get("iaqi", {})

        return {
            "city": raw.get("city", {}).get("name", "Unknown"),
            "latitude": raw.get("city", {}).get("geo", [None, None])[0],
            "longitude": raw.get("city", {}).get("geo", [None, None])[1],
            "aqi_value": raw.get("aqi") if str(raw.get("aqi", "")).isdigit() else None,
            "dominant_pollutant": raw.get("dominentpol", None),
            "pollutants": {
                "pm25": iaqi.get("pm25", {}).get("v"),
                "pm10": iaqi.get("pm10", {}).get("v"),
                "o3":   iaqi.get("o3",   {}).get("v"),
                "no2":  iaqi.get("no2",  {}).get("v"),
                "so2":  iaqi.get("so2",  {}).get("v"),
                "co":   iaqi.get("co",   {}).get("v"),
            },
            "weather": {
                "temperature": iaqi.get("t",  {}).get("v"),
                "humidity":    iaqi.get("h",  {}).get("v"),
                "wind_speed":  iaqi.get("w",  {}).get("v"),
            },
            "recorded_at": raw.get("time", {}).get("iso"),
            "raw_data": raw
        }