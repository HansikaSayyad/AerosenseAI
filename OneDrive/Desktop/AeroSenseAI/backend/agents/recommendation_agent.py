# backend/agents/recommendation_agent.py

from datetime import datetime
from backend.agents.base_agent import BaseAgent, AgentResult


class RecommendationAgent(BaseAgent):
    """
    Responsible for:
    - Generating health recommendations
    - Considering AQI level
    - Advising sensitive groups
    """

    # ─────────────────────────────────────────
    # RECOMMENDATION RULES
    # ─────────────────────────────────────────
    RECOMMENDATIONS = {
        "Good": {
            "general_advice": "Air quality is good. Enjoy outdoor activities!",
            "outdoor_activity": "safe",
            "mask_required": "no",
            "window_advice": "open",
            "sensitive_groups": []
        },
        "Moderate": {
            "general_advice": "Air quality is acceptable. Unusually sensitive people should limit prolonged outdoor exertion.",
            "outdoor_activity": "safe",
            "mask_required": "optional",
            "window_advice": "open",
            "sensitive_groups": [
                "People with respiratory issues should monitor symptoms"
            ]
        },
        "Unhealthy for Sensitive Groups": {
            "general_advice": "Sensitive groups may experience health effects. General public is less likely to be affected.",
            "outdoor_activity": "limited",
            "mask_required": "optional",
            "window_advice": "open",
            "sensitive_groups": [
                "Children should limit outdoor activities",
                "Elderly should avoid prolonged outdoor exposure",
                "People with asthma should carry inhaler",
                "Heart patients should avoid exertion"
            ]
        },
        "Unhealthy": {
            "general_advice": "Everyone may begin to experience health effects. Sensitive groups may experience more serious effects.",
            "outdoor_activity": "limited",
            "mask_required": "yes",
            "window_advice": "closed",
            "sensitive_groups": [
                "Children must avoid outdoor activities",
                "Elderly must stay indoors",
                "Asthma patients must use medication",
                "Everyone should wear N95 mask outdoors"
            ]
        },
        "Very Unhealthy": {
            "general_advice": "Health alert! Everyone may experience serious health effects.",
            "outdoor_activity": "avoid",
            "mask_required": "yes",
            "window_advice": "closed",
            "sensitive_groups": [
                "All sensitive groups must stay indoors",
                "Use air purifiers indoors",
                "Seal windows and doors",
                "Avoid all outdoor physical activity"
            ]
        },
        "Hazardous": {
            "general_advice": "Health warning of emergency conditions. Everyone is affected.",
            "outdoor_activity": "avoid",
            "mask_required": "yes",
            "window_advice": "closed",
            "sensitive_groups": [
                "Emergency conditions — stay indoors",
                "Use N95/N99 masks if going out",
                "Run air purifiers continuously",
                "Seek medical attention if experiencing symptoms"
            ]
        },
        "Unknown": {
            "general_advice": "Air quality data unavailable. Take precautions if air looks hazy.",
            "outdoor_activity": "limited",
            "mask_required": "optional",
            "window_advice": "open",
            "sensitive_groups": []
        }
    }

    def __init__(self):
        super().__init__(name="RecommendationAgent")

    def run(self, input_data: dict) -> AgentResult:
        """
        Accepts analyzed data from AnalysisAgent.
        Returns personalized recommendations.
        """
        start_time = datetime.now()

        try:
            category = input_data.get("aqi_category", "Unknown")
            rules = self.RECOMMENDATIONS.get(
                category,
                self.RECOMMENDATIONS["Unknown"]
            )

            recommendation = {
                **input_data,
                "recommendations": {
                    "aqi_category": category,
                    "general_advice": rules["general_advice"],
                    "outdoor_activity": rules["outdoor_activity"],
                    "mask_required": rules["mask_required"],
                    "window_advice": rules["window_advice"],
                    "sensitive_groups": rules["sensitive_groups"]
                }
            }

            return self.success_result(
                data=recommendation,
                execution_time_ms=self._track_time(start_time)
            )

        except Exception as e:
            return self.error_result(
                f"Recommendation failed: {str(e)}",
                self._track_time(start_time)
            )