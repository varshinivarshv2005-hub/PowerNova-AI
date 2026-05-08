import sqlite3
import pandas as pd
import os

# Get project root path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database file path
DB_NAME = os.path.join(BASE_DIR, "database", "powernova.db")


# Create table
def create_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS electricity_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            usage_kwh REAL,
            voltage REAL,
            current REAL
        )
    """)

    conn.commit()
    conn.close()


# Insert data
def insert_data(data):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO electricity_data
        (timestamp, usage_kwh, voltage, current)
        VALUES (?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["usage_kwh"],
        data["voltage"],
        data["current"]
    ))

    conn.commit()
    conn.close()


# Fetch all data
def fetch_data():

    conn = sqlite3.connect(DB_NAME)

    query = "SELECT * FROM electricity_data"

    df = pd.read_sql(query, conn)

    conn.close()

    return df