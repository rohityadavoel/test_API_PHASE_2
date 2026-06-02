# Consulting Platform Backend

## Prerequisites
- Python 3.11+
- PostgreSQL 15+

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` or `venv\Scripts\activate` on Windows
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file based on `.env.example`
6. Create PostgreSQL database: `createdb consulting_db`

## Run Migrations
```bash
alembic upgrade head
```

## Run Seed
```bash
python seed.py
```

## Start Server
```bash
uvicorn app.main:app --reload
```

## API Docs
http://localhost:8000/docs
