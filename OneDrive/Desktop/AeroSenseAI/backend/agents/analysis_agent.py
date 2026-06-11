# backend/agents/analysis_agent.py

from datetime import datetime
from backend.agents.base_agent import BaseAgent, AgentResult


class AnalysisAgent(BaseAgent):
    """
    Responsible for:
    - Determining AQI category from value
    - Identifying dominant pollutant
    - Detecting anomalies
    """

    # ─────────────────────────────────────────
    # AQI CATEGORIES — WHO Standard
    # ─────────────────────────────────────────
    AQI_CATEGORIES = [
        (0,   50,  "Good",                 "green"),
        (51,  100, "Moderate",             "yellow"),
        (101, 150, "Unhealthy for Sensitive Groups", "orange"),
        (151, 200, "Unhealthy",            "red"),
        (201, 300, "Very Unhealthy",       "purple"),
        (301, 500, "Hazardous",            "maroon"),
    ]

    def __init__(self):
        super().__init__(name="AnalysisAgent")

    def run(self, input_data: dict) -> AgentResult:
        """
        Accepts normalized data from DataCollectionAgent.
        Returns analysis with category, dominant pollutant.
        """
        start_time = datetime.now()

        try:
            aqi_value = input_data.get("aqi_value")
            pollutants = input_data.get("pollutants", {})

            # ─────────────────────────────────────────
            # GET AQI CATEGORY
            # ─────────────────────────────────────────
            category, color = self._get_category(aqi_value)

            # ─────────────────────────────────────────
            # GET DOMINANT POLLUTANT
            # ─────────────────────────────────────────
            dominant = self._get_dominant_pollutant(
                input_data.get("dominant_pollutant"),
                pollutants
            )

            # ─────────────────────────────────────────
            # DETECT ANOMALIES
            # ─────────────────────────────────────────
            anomalies = self._detect_anomalies(pollutants)

            analysis = {
                **input_data,
                "aqi_category": category,
                "aqi_color": color,
                "dominant_pollutant": dominant,
                "anomalies": anomalies,
                "health_risk_level": self._get_risk_level(aqi_value)
            }

            return self.success_result(
                data=analysis,
                execution_time_ms=self._track_time(start_time)
            )

        except Exception as e:
            return self.error_result(
                f"Analysis failed: {str(e)}",
                self._track_time(start_time)
            )

    def _get_category(self, aqi_value) -> tuple:
        """Returns AQI category and color"""
        if aqi_value is None:
            return "Unknown", "gray"
        try:
            aqi = int(aqi_value)
            for low, high, category, color in self.AQI_CATEGORIES:
                if low <= aqi <= high:
                    return category, color
            return "Hazardous", "maroon"
        except (ValueError, TypeError):
            return "Unknown", "gray"

    def _get_dominant_pollutant(self, api_dominant: str, pollutants: dict) -> str:
        """Returns dominant pollutant"""
        if api_dominant:
            return api_dominant
        if not pollutants:
            return "Unknown"
        valid = {k: v for k, v in pollutants.items() if v is not None}
        if not valid:
            return "Unknown"
        return max(valid, key=valid.get)

    def _detect_anomalies(self, pollutants: dict) -> list:
        """Detects unusually high pollutant levels"""
        thresholds = {
            "pm25": 150,
            "pm10": 250,
            "o3": 200,
            "no2": 200,
            "so2": 350,
            "co": 30
        }
        anomalies = []
        for pollutant, threshold in thresholds.items():
            value = pollutants.get(pollutant)
            if value and value > threshold:
                anomalies.append({
                    "pollutant": pollutant,
                    "value": value,
                    "threshold": threshold,
                    "message": f"{pollutant.upper()} is critically high!"
                })
        return anomalies

    def _get_risk_level(self, aqi_value) -> str:
        """Returns simple risk level"""
        if aqi_value is None:
            return "unknown"
        try:
            aqi = int(aqi_value)
            if aqi <= 50:   return "low"
            if aqi <= 100:  return "moderate"
            if aqi <= 150:  return "high"
            return "critical"
        except (ValueError, TypeError):
            return "unknown"