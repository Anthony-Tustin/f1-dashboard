# F1 Dashboard

A full-stack data engineering project that takes live Formula One data and displays it through a locally-hosted web dashboard.

Data is automatically fetch every hour from the official F1 timing 
API is the FastF1 Python library, stored in a PostgreSQL database, 
and passed through a FastAPI REST backend to a simple HTML/CSS/JS frontend.

# Features include:

- Live 2025 driver and constructor championship standings
- Race results, qualifying grids, lap times and sector splits
- Pit stop data and race weather conditions
- Automatic hourly data refresh via APScheduler
- Manual refresh button with live feedback in the UI

# Tech libraries:

| Data Source | FastF1 Python Library |
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy (async) |
| Scheduling | APScheduler |
| Frontend | HTML, CSS, JavaScript |

# Project Structure
```
f1-dashboard/
├── app/
│   ├── ingestion/       # FastF1 data fetching and database upserts
│   ├── routers/         # FastAPI endpoint definitions
│   ├── database.py      # Async PostgreSQL connection
│   ├── models.py        # SQLAlchemy table definitions
│   ├── scheduler.py     # Hourly refresh scheduler
│   └── main.py          # FastAPI app entry point
├── static/              # Frontend HTML, CSS, JavaScript
└── .env.example         # Environment template
```

---

# Setup Instructions

# Prerequisites to run application
- Python 3.12+
- PostgreSQL 16+

# 1. Clone the repository
```bash
git clone https://github.com/Anthony-Tustin/f1-dashboard.git
cd f1-dashboard
```

# 2. Create and activate a virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 4. Create a PostgreSQL database
```bash
psql -U postgres -c "CREATE DATABASE f1_dashboard;"
```

# 5. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your PostgreSQL credentials.

# 6. Start the server
```bash
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000/static/index.html`

API documentation is available at `http://localhost:8000/docs`


# How It Works

1. On startup the server creates database tables automatically
2. APScheduler triggers a data refresh every hour in the background
3. FastF1 fetches current season data from the official F1 timing API
4. Data is upserted (updated) into PostgreSQL using ON CONFLICT DO UPDATE (old vs new data)
5. FastAPI serves the data through REST endpoints (specific URL - digital address where an API recieves requirest and sends back data)
6. The frontend fetches data from the API on page load and displays it

# Skills Demonstrated in my portfolio project

- Relational database design with foreign keys and unique constraints
- Async Python using FastAPI and SQLAlchemy
- ETL pipeline design — Extract (FastF1), Transform (pandas), Load (PostgreSQL)
- REST API design with automatic documentation
- Scheduled background tasks
- Frontend data UI using HTML, CSS and JavaScript