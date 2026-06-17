# AirGuard AI - Agentic Air Quality Monitoring and Recommendation Platform

## Tech Stack
- Backend: FastAPI, Python 3.13
- Database: PostgreSQL 18, SQLAlchemy
- Security: JWT, bcrypt, RBAC
- AI Agents: DataCollectionAgent, AnalysisAgent, RecommendationAgent
- Frontend: React + TypeScript + TailwindCSS (coming next)

## Project Structure
- `backend/agents/` - AI Agent classes
- `backend/services/` - Business logic
- `backend/repositories/` - Database queries
- `backend/models/` - SQLAlchemy models
- `backend/schemas/` - Pydantic schemas
- `backend/security/` - JWT, password, RBAC
- `backend/database/` - PostgreSQL connection
- `backend/core/` - Config and settings
- `backend/api/v1/` - FastAPI routes

## Database
Database credentials are stored in `.env` file.

## Running the Server
```
uvicorn backend.main:app --reload --port 8001
```
- API: http://127.0.0.1:8001
- Swagger UI: http://127.0.0.1:8001/docs

## Current Phase
Phase 1 complete - Backend done, starting React Frontend next.

## Important Rules
- Always use a virtual environment (venv)
- Never hardcode credentials
- Follow SOLID principles
- All agents must implement the `agent.run(input_data)` interface
- Keep agent design future-compatible with LangGraph
