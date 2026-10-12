import logging
import os
from datetime import date
from pathlib import Path

import psycopg2
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def get_session(user_agent: str | None = None) -> requests.Session:
    """HTTP session that retries on rate limits and server errors."""
    retry = Retry(total=5, backoff_factor=1,
                  status_forcelist=[429, 500, 502, 503, 504])
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    if user_agent:
        session.headers["User-Agent"] = user_agent
    return session


def raw_path(source: str, run_date: date) -> Path:
    """Folder like data/raw/source=fred/date=2026-10-12/"""
    path = RAW_DIR / f"source={source}" / f"date={run_date.isoformat()}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )