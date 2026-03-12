import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    retries = 5
    while retries > 0:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            cur.close()
            conn.close()

            return f"""
            <h1>Aplikacja działa</h1>
            <p>Połączenie z bazą PostgreSQL zostało nawiązane.</p>
            <p><b>Wersja bazy:</b> {db_version}</p>
            """
        except Exception as e:
            retries -= 1
            time.sleep(2)
            last_error = str(e)

    return f"<h1>Błąd połączenia z bazą</h1><p>{last_error}</p>", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)