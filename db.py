import sqlite3
import pandas as pd

DB_PATH = "aqua_track.db"

def init_db():
    """Initialize the database and create the sensor_data table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            ph REAL,
            dissolved_oxygen REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(temperature: float, ph: float, dissolved_oxygen: float):
    """Insert a new sensor reading into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sensor_data (temperature, ph, dissolved_oxygen)
        VALUES (?, ?, ?)
    ''', (temperature, ph, dissolved_oxygen))
    conn.commit()
    conn.close()

def fetch_recent(limit: int = 200) -> pd.DataFrame:
    """Fetch the most recent sensor data as a pandas DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT {limit}",
        conn
    )
    conn.close()
    return df

def fetch_all() -> pd.DataFrame:
    """Fetch all sensor data for analysis."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensor_data ORDER BY timestamp ASC", conn)
    conn.close()
    return df

# Initialize the database when this module is run directly
if __name__ == "__main__":
    init_db()
    print("Database initialized and ready!")