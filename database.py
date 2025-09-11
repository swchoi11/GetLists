# database.py

import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESTAURANT_DB_PATH = os.path.join(BASE_DIR, "restaurant.db")

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # restaurants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                rating REAL,
                address TEXT,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
        
        conn.commit()
        conn.close()

    def add_restaurant(self, name, description=None, category=None, rating=None, address=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO restaurants (name, description, category, rating, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, category, rating, address))
        conn.commit()
        rid = cursor.lastrowid
        conn.close()
        return rid

    def get_all_restaurants(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description, category, rating, address, create_time
            FROM restaurants
            ORDER BY create_time DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_restaurant_by_id(self, restaurant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description, category, rating, address, create_time
            FROM restaurants
            WHERE id = ?
            """, (restaurant_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def update_restaurant(self, restaurant_id: int, **fields):
        # fields 딕셔너리에서 none 아닌 것만 업뎃
        sets = []
        values = []
        for k, v in fields.items():
            if v is not None and k in {"name", "description", "category", "rating", "address"}:
                sets.append(f"{k} = ?")
                values.append(v)
        if not sets:
            return 0
        
        values.append(restaurant_id)
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE restaurants
            SET {", ".join(sets)}
            WHERE id = ?
        """, tuple(values))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount

    def delete_restaurant(self, restaurant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurants WHERE id = ?",
            (restaurant_id,))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount

db_restaurant = DatabaseManager(RESTAURANT_DB_PATH)