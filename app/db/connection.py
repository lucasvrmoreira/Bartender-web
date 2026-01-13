import psycopg2
from psycopg2.extras import RealDictCursor
import os

from app.config import DATABASE_URL, SCHEMA


def get_conn():
    conn_args = {
        "dsn": DATABASE_URL,
        "cursor_factory": RealDictCursor
    }

    # 🔐 SSL só em produção
    if os.getenv("APP_ENV") == "production":
        conn_args["sslmode"] = "require"

    conn = psycopg2.connect(**conn_args)

    cur = conn.cursor()
    cur.execute(f"SET search_path TO {SCHEMA};")
    cur.close()

    return conn
