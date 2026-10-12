import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# 1. FRED
r = requests.get(
    "https://api.stlouisfed.org/fred/series/observations",
    params={"series_id": "CPIAUCSL", "api_key": os.getenv("FRED_API_KEY"),
            "file_type": "json", "limit": 3},
)
print("FRED:", r.status_code, r.json()["observations"][0])

# 2. SEC EDGAR (Apple)
r = requests.get(
    "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json",
    headers={"User-Agent": os.getenv("SEC_USER_AGENT")},
)
print("EDGAR:", r.status_code, r.json()["entityName"])

# 3. Postgres
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"),
    user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DB"),
)
print("Postgres:", conn.server_version)
conn.close()