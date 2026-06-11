# backend/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel


# ─────────────────────────────────────────
# AGENT RESULT — standardized output
# Every agent returns this same structure
# ─────────────────────────────────────────
class AgentResult(BaseModel):
    """
    Standardized result returned by every agent.
    This makes agents composable and predictable.
    """
    success: bool
    agent_name: str
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None
    timestamp: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True


# ─────────────────────────────────────────
# BASE AGENT — parent class
# All agents inherit from this
# ─────────────────────────────────────────
class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.

    Design Principles:
    - Every agent has a standard run() method
    - Every agent returns AgentResult
    - Agents are independent and reusable
    - Future-compatible with LangGraph nodes

    Usage:
        class MyAgent(BaseAgent):
            def run(self, input_data):
                ...
    """

    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()

    @abstractmethod
    def run(self, input_data: Any) -> AgentResult:
        """
        Main entry point for every agent.
        Must be implemented by all subclasses.
        """
        pass

    def success_result(self, data: Any, execution_time_ms: float = None) -> AgentResult:
        """Helper to create a successful AgentResult"""
        return AgentResult(
            success=True,
            agent_name=self.name,
            data=data,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )

    def error_result(self, error: str, execution_time_ms: float = None) -> AgentResult:
        """Helper to create a failed AgentResult"""
        return AgentResult(
            success=False,
            agent_name=self.name,
            error=error,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )

    def _track_time(self, start_time: datetime) -> float:
        """Calculate execution time in milliseconds"""
        end_time = datetime.now()
        delta = end_time - start_time
        return delta.total_seconds() * 1000

    def __repr__(self):
        return f"<Agent: {self.name}>"