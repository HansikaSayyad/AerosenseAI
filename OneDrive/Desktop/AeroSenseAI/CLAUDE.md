# AirGuard AI — Agentic Air Quality Monitoring & Recommendation Platform

## Project Overview

AirGuard AI is a full-stack, production-grade web application that fetches real-time air quality
data from the WAQI API, processes it through a 3-agent AI pipeline, and presents health
recommendations on a modern React dashboard. Authentication is JWT-based with RBAC. Every
search made by a logged-in user is automatically saved to PostgreSQL and visible in a History page.

The agent architecture is intentionally designed to be forward-compatible with LangGraph —
each agent implements `agent.run(input_data)` so they can be plugged into a LangGraph graph
as nodes in a future phase without changing the agent internals.

---

## Current Phase Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Project scaffold, venv, folder structure | Complete |
| Phase 1 | Backend — FastAPI, agents, DB, JWT, RBAC | Complete |
| Phase 2 | React frontend — pages, components, routing | Complete |
| Phase 3 | Frontend + Backend API connection | Complete |
| Phase 4 | History page, Profile page, bug fixes | Complete |
| Phase 5 | Deployment (Docker, AWS/Railway) | Next |
| Phase 6 | LangGraph orchestration, Redis, new agents | Future |

---

## Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.13 | Runtime |
| FastAPI | latest | REST API framework |
| Uvicorn | 0.49.0 | ASGI server |
| SQLAlchemy | 2.0.50 | ORM |
| Alembic | 1.18.4 | Database migrations |
| PostgreSQL | 18 | Primary database |
| psycopg2-binary | 2.9.12 | PostgreSQL driver |
| Pydantic | v2 | Data validation and settings |
| pydantic-settings | latest | .env config loading |
| python-jose | 3.5.0 | JWT token creation/verification |
| passlib + bcrypt | 1.7.4 / 4.0.1 | Password hashing |
| requests | 2.32.5 | WAQI API HTTP calls |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.7 | UI framework |
| TypeScript | 6.0.2 | Type safety |
| Vite | 8.0.12 | Build tool and dev server |
| TailwindCSS | 4.3.1 | Utility-first styling |
| @tailwindcss/vite | 4.3.1 | Tailwind v4 Vite plugin |
| React Router | 7.18.0 | Client-side routing |
| Axios | 1.18.0 | HTTP client |
| Recharts | 3.8.1 | Pollutants bar chart |

### External APIs
| API | Purpose |
|-----|---------|
| WAQI (World Air Quality Index) | Real-time AQI data by city or GPS coordinates |

---

## Folder Structure

```
AeroSenseAI/
├── .env                              # Secrets — never commit this file
├── CLAUDE.md                         # This file
├── requirements.txt                  # Python dependencies
├── backend/
│   ├── main.py                       # FastAPI app, CORS, lifespan, health routes
│   ├── agents/
│   │   ├── base_agent.py             # Abstract BaseAgent + AgentResult schema
│   │   ├── data_collection_agent.py  # Fetches + normalizes AQI from WAQI API
│   │   ├── analysis_agent.py         # AQI category, anomalies, health_risk_level
│   │   └── recommendation_agent.py   # Health advice by AQI category
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py           # api_router with prefix /api/v1
│   │       ├── auth.py               # /auth routes (register, login, me, refresh)
│   │       └── aqi.py                # /aqi routes (city, gps, history)
│   ├── core/
│   │   └── config.py                 # Pydantic Settings — loads all .env values
│   ├── database/
│   │   └── connection.py             # SQLAlchemy engine, SessionLocal, get_db
│   ├── models/
│   │   ├── user.py                   # User table (UUID PK, RBAC roles enum)
│   │   ├── location.py               # Locations per user (city + GPS)
│   │   ├── aqi_reading.py            # AQI readings (pollutants + weather + raw_data)
│   │   └── recommendation.py         # Recommendations linked to readings
│   ├── repositories/
│   │   ├── user_repository.py        # User CRUD queries
│   │   ├── location_repository.py    # Location queries
│   │   └── aqi_repository.py         # AQI reading queries
│   ├── schemas/
│   │   ├── user.py                   # UserCreate, UserLogin, UserResponse, Token
│   │   ├── aqi.py                    # AQIByCity, AQIByGPS, AQIResponse
│   │   └── recommendation.py         # Recommendation schemas
│   ├── security/
│   │   ├── jwt_handler.py            # Create/verify access + refresh tokens
│   │   ├── password_handler.py       # bcrypt hash + verify
│   │   └── rbac.py                   # require_auth, optional_auth, require_admin
│   └── services/
│       ├── user_service.py           # register, login, get_profile, refresh_token
│       └── aqi_service.py            # 3-agent pipeline + DB save + history fetch
└── frontend/
    ├── index.html                    # Entry HTML — mounts div#root
    ├── vite.config.ts                # Vite + React plugin + Tailwind v4 plugin, port 5173
    ├── tsconfig.json                 # TypeScript strict mode, JSX react-jsx
    ├── package.json                  # npm dependencies
    └── src/
        ├── main.tsx                  # React root mount (StrictMode)
        ├── App.tsx                   # BrowserRouter + AuthProvider + Routes
        ├── index.css                 # @import "tailwindcss" (Tailwind v4 syntax)
        ├── api/
        │   ├── client.ts             # Axios instance — JWT interceptor, 401 logout
        │   ├── auth.ts               # authApi: register, login, me, refresh
        │   └── aqi.ts                # aqiApi: getByCity, getByGPS, getHistory
        ├── context/
        │   └── AuthContext.tsx       # AuthProvider + useAuth hook + session restore
        ├── components/
        │   ├── Navbar.tsx            # Sticky nav — Dashboard/History/Profile links
        │   ├── ProtectedRoute.tsx    # Redirects to /login if not authenticated
        │   ├── AQICard.tsx           # AQI value card with category color coding
        │   ├── PollutantsChart.tsx   # Recharts bar chart for all pollutants
        │   └── RecommendationsCard.tsx  # AI recommendations (flat string display)
        ├── pages/
        │   ├── Login.tsx             # Login form — JWT — redirect to /dashboard
        │   ├── Register.tsx          # Register form (username + email + password rules)
        │   ├── Dashboard.tsx         # City search + GPS + full AQI results
        │   ├── History.tsx           # Past AQI searches from DB (logged-in users only)
        │   └── Profile.tsx           # User details (name, email, role, join date)
        ├── types/
        │   ├── auth.ts               # User, LoginRequest, RegisterRequest, TokenResponse
        │   └── aqi.ts                # AQIResponse, Pollutants, HistoryEntry
        └── utils/
            └── aqiColors.ts          # AQI category → Tailwind classes + hex + emoji
```

---

## Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/airguard_db

# JWT Security
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# WAQI AQI API
AQI_API_KEY=<your-waqi-api-key>
AQI_BASE_URL=https://api.waqi.info

# App Settings
APP_NAME=AirGuard AI
APP_VERSION=1.0.0
DEBUG=True

# CORS — must be a JSON array, must include the Vite dev server port
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173","http://127.0.0.1:5173","http://localhost:5174","http://127.0.0.1:5174"]
```

Note: ALLOWED_ORIGINS must be a valid JSON array (not comma-separated), otherwise pydantic-settings
will fail to parse it.

---

## Database Schema

### users
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| email | String | Unique, indexed |
| username | String | Unique, indexed |
| hashed_password | String | bcrypt |
| full_name | String | Optional display name |
| role | Enum | user / admin / premium |
| is_active | Boolean | Default true |
| is_verified | Boolean | Default false |
| created_at | DateTime | Auto |
| last_login | DateTime | Updated on each login |

### locations
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| user_id | UUID | FK → users |
| city | String | e.g. "Hyderabad" |
| latitude | Float | GPS lat |
| longitude | Float | GPS lon |
| is_default | Boolean | User's primary location |

### aqi_readings
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| location_id | UUID | FK → locations |
| aqi_value | Integer | 0–500 |
| aqi_category | String | Good / Moderate / Unhealthy / etc. |
| dominant_pollutant | String | pm25, pm10, o3... |
| pm25, pm10, o3, no2, so2, co | Float | Individual pollutant values |
| temperature, humidity, wind_speed | Float | Weather data |
| raw_data | JSON | Full WAQI API response |
| recorded_at | DateTime | Timestamp from WAQI API |

### recommendations
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| user_id | UUID | FK → users |
| aqi_reading_id | UUID | FK → aqi_readings |
| aqi_category | String | Category at time of reading |
| general_advice | Text | Free text health advice |
| outdoor_activity | String | safe / limited / avoid |
| mask_required | String | yes / no / optional |
| window_advice | String | open / closed |
| sensitive_groups | JSON | Array of strings |

---

## API Endpoints

### Authentication — /api/v1/auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/v1/auth/register | None | Create account. Returns user + tokens. |
| POST | /api/v1/auth/login | None | Login. Returns user + tokens. |
| GET | /api/v1/auth/me | Bearer | Get current user profile. |
| POST | /api/v1/auth/refresh | None | Exchange refresh token for new access token. |

Register/Login response shape:
```json
{
  "success": true,
  "message": "Registration successful",
  "user": { "id", "email", "username", "role" },
  "tokens": { "access_token", "refresh_token", "token_type" }
}
```

Registration rules:
- username: 3+ chars, alphanumeric only
- password: 8+ chars, at least 1 uppercase letter, at least 1 number
- email: valid email format

### Air Quality — /api/v1/aqi

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/aqi/city?city=Hyderabad | Optional | Real-time AQI for a city. Saves to DB if logged in. |
| POST | /api/v1/aqi/gps | Optional | AQI by { latitude, longitude }. Saves to DB if logged in. |
| GET | /api/v1/aqi/history?limit=20 | Required | User's saved AQI search history. |

GPS request body:
```json
{ "latitude": 17.38, "longitude": 78.48 }
```

AQI response shape:
```json
{
  "success": true,
  "city": "Somajiguda, Hyderabad, India",
  "aqi_value": 65,
  "aqi_category": "Moderate",
  "dominant_pollutant": "pm25",
  "health_risk_level": "moderate",
  "pollutants": { "pm25": 65, "pm10": 63, "o3": 16, "no2": 4, "so2": 3, "co": 44 },
  "weather": { "temperature": null, "humidity": 26.73, "wind_speed": null },
  "recommendations": {
    "aqi_category": "Moderate",
    "general_advice": "Air quality is acceptable for most people...",
    "outdoor_activity": "safe",
    "mask_required": "optional",
    "window_advice": "open",
    "sensitive_groups": ["People with respiratory issues should monitor symptoms"]
  },
  "recorded_at": "2026-06-17T16:00:00+05:30"
}
```

History response shape:
```json
{
  "success": true,
  "history": [
    {
      "id": "uuid",
      "city": "Hyderabad",
      "aqi_value": 65,
      "aqi_category": "Moderate",
      "dominant_pollutant": "pm25",
      "recorded_at": "...",
      "created_at": "..."
    }
  ]
}
```

### System Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check — app name, version, status |
| GET | /health | Database connectivity check |
| GET | /test-agents?city=Hyderabad | Run full 3-agent pipeline test |
| GET | /docs | Swagger UI |
| GET | /redoc | ReDoc UI |

---

## Agent Pipeline

```
User Request (city or GPS)
        |
        v
DataCollectionAgent.run({"city": "Hyderabad"})
  Calls WAQI API → normalizes response
  Output: city, aqi_value, pollutants{pm25,pm10,o3,no2,so2,co}, weather{temp,humidity,wind}
        |
        v
AnalysisAgent.run(normalized_data)
  Assigns AQI category (Good / Moderate / Unhealthy for Sensitive Groups / Unhealthy / Very Unhealthy / Hazardous)
  Detects anomalies (pm25 > 150, pm10 > 250, etc.)
  Sets health_risk_level (low / moderate / high / critical)
        |
        v
RecommendationAgent.run(analyzed_data)
  Looks up rule table for the AQI category
  Returns: general_advice, outdoor_activity, mask_required, window_advice, sensitive_groups[]
        |
        v
Response returned to API → saved to DB (authenticated users only) → sent to frontend
```

All agents extend `BaseAgent` and return `AgentResult`:
```python
class AgentResult(BaseModel):
    success: bool
    agent_name: str
    data: Optional[dict]
    error: Optional[str]
    execution_time_ms: float
    timestamp: str
```

### AQI Categories (US EPA Standard)
| Range | Category |
|-------|----------|
| 0–50 | Good |
| 51–100 | Moderate |
| 101–150 | Unhealthy for Sensitive Groups |
| 151–200 | Unhealthy |
| 201–300 | Very Unhealthy |
| 301–500 | Hazardous |

---

## How to Run the Project

### Prerequisites
- Python 3.13
- Node.js 22+
- PostgreSQL 18 running locally
- Database `airguard_db` created in PostgreSQL
- `.env` file set up with real credentials

### Backend
```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Run server
uvicorn backend.main:app --reload --port 8001
```

- API: http://127.0.0.1:8001
- Swagger UI: http://127.0.0.1:8001/docs

### Frontend
```bash
cd frontend
npm run dev
```

- App: http://localhost:5173

Note: If port 5173 is already in use, Vite will fail because `strictPort: true` is set.
Kill the process on that port or close the conflicting app before running.

### Running Both Together (two terminals)
```
Terminal 1 (backend):  uvicorn backend.main:app --reload --port 8001
Terminal 2 (frontend): cd frontend && npm run dev
```

---

## Frontend Routes

| Route | Auth Required | Page |
|-------|--------------|------|
| /login | No | Login form |
| /register | No | Registration form |
| /dashboard | Yes | AQI search + results + charts |
| /history | Yes | Past AQI searches |
| /profile | Yes | User account details |
| /* | — | Redirects to /dashboard |

---

## Architecture Decisions

### Repository Pattern
All database queries live in `repositories/`. Services call repositories, never raw SQLAlchemy.
This makes swapping the database engine straightforward.

### Service Layer
Business logic lives in `services/`. FastAPI route handlers call services and return the result.
Routes contain zero business logic — they only validate input and format responses.

### Dependency Injection
FastAPI's `Depends()` is used throughout:
- `get_db` → injects a SQLAlchemy session per request
- `rbac.require_auth` / `rbac.optional_auth` → injects parsed JWT payload

### Agent Interface
All agents extend `BaseAgent` and implement `agent.run(input_data) -> AgentResult`.
This standardized interface makes agents:
- Independently testable (each agent can be unit tested in isolation)
- Composable (output of one feeds directly into the next)
- LangGraph-ready (can be registered as graph nodes without internal changes)

### Optional Auth on AQI Endpoints
`GET /aqi/city` and `POST /aqi/gps` use `rbac.optional_auth` (HTTPBearer with `auto_error=False`).
- Unauthenticated users get AQI data but nothing is saved to DB
- Authenticated users get AQI data AND it is automatically saved to their history

### JWT Strategy
- Access token: 30 minutes — sent in every API request header
- Refresh token: 7 days — stored in localStorage, used only to get new access tokens
- Axios interceptor attaches `Authorization: Bearer <token>` to every outgoing request
- On 401 response: tokens cleared from localStorage, user redirected to /login

### Tailwind CSS v4
Uses `@tailwindcss/vite` plugin instead of the legacy PostCSS approach.
Entry CSS file uses `@import "tailwindcss"` — no `tailwind.config.js` needed.

### CORS Configuration
ALLOWED_ORIGINS is loaded from `.env` via pydantic-settings as a JSON array.
The Vite dev server ports (5173, 5174) must be included or all API requests will fail
with a 400 error on OPTIONS preflight.

---

## Known Behaviors (Not Bugs)

- Small or obscure cities (e.g. "vinukonda") return `"Unknown station"` from the WAQI API.
  This is expected — WAQI does not have monitoring stations everywhere. The frontend shows
  an appropriate error message.
- Some pollutant values (e.g. temperature, wind_speed) may be `null` if the monitoring
  station does not report them. The frontend displays `—` in those cases.

---

## Future Plans

### Phase 5 — Deployment
- Dockerize backend and frontend separately
- Docker Compose for local full-stack development
- Deploy backend to Railway or AWS EC2
- Deploy frontend to Vercel or Netlify
- GitHub Actions CI/CD pipeline (lint, test, deploy on push to main)
- Environment configs: dev / staging / prod

### Phase 6 — LangGraph Upgrade
Migration plan: 80–90% of existing code is reused as-is.

```
Current pipeline (sequential, stateless):
DataCollectionAgent → AnalysisAgent → RecommendationAgent

Future pipeline (LangGraph StateGraph):
  - DataCollectionAgent  (existing node, unchanged)
  - AnalysisAgent        (existing node, unchanged)
  - RecommendationAgent  (existing node, unchanged)
  - WeatherAgent         (new — correlates weather patterns with AQI trends)
  - ForecastAgent        (new — predicts AQI 24–48 hours ahead)
  - AlertAgent           (new — triggers push/email alerts at threshold breaches)
  - ReportingAgent       (new — weekly PDF/email health reports)
```

New technology for Phase 6:
- LangGraph (graph-based agent orchestration + shared state)
- Anthropic Claude API (natural language, context-aware recommendations)
- Redis (response caching + pub/sub for real-time alerts)
- Celery (background tasks: forecast jobs, report generation)

### Other Planned Features
- AQI trend charts (7-day and 30-day graphs on the History page)
- Email/push notifications when AQI crosses a user-set threshold
- Multiple saved locations per user (not just the last searched)
- PWA support (offline-capable, installable on mobile)
- Admin dashboard to monitor all users and system health

---

## Important Rules
- Always use the virtual environment (`venv`)
- Never hardcode credentials — everything goes in `.env`
- Never commit `.env` to git (add to `.gitignore`)
- Follow SOLID principles throughout
- All agents must implement `agent.run(input_data)` returning `AgentResult`
- Services contain business logic — routes do not
- Repositories contain DB queries — services do not write raw SQL
- ALLOWED_ORIGINS in `.env` must be a JSON array, not a comma-separated string
