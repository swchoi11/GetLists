# database.py
## 데이터 접근 레이어(DAO/Repository)
## 스키마 초기화, SQL 작성/실행, 트랜잭션/커넥션 관리, 결과 반환

import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESTAURANT_DB_PATH = os.path.join(BASE_DIR, "restaurant.db")
CAFE_DB_PATH = os.path.join(BASE_DIR, "cafe.db")

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
        
        # cafe table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cafes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cafe_name TEXT NOT NULL,
                description TEXT,
                rating REAL,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
      
    def add_cafe(self, cafe_name, description=None, rating=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cafes (cafe_name, description, rating)
            VALUES (?, ?, ?)
        ''', (cafe_name, description, rating))
        
        conn.commit()
        cafe_id = cursor.lastrowid
        conn.close()
        return cafe_id

    # 전체 조회
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

    # 단일 조회
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
        
    def get_all_cafes(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, cafe_name, description, rating, create_time
            FROM cafes
            ORDER BY create_time DESC
        ''')
        
        cafes = cursor.fetchall()
        conn.close()
        return cafes

    def get_cafe_by_id(self, cafe_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, cafe_name, description, rating, create_time
            FROM cafes
            WHERE id = ?
        ''', (cafe_id,))
        
        cafe = cursor.fetchone()
        conn.close()
        return cafe
    
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
      
    def update_cafe(self, cafe_id, cafe_name=None, description=None, rating=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        updates = []
        params = []
        
        if cafe_name is not None:
            updates.append("cafe_name = ?")
            params.append(cafe_name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if rating is not None:
            updates.append("rating = ?")
            params.append(rating)
        
        if not updates:
            conn.close()
            return
            
        params.append(cafe_id)
        query = f"UPDATE cafes SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def delete_restaurant(self, restaurant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurants WHERE id = ?",
            (restaurant_id,))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount

    def delete_cafe(self, cafe_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM cafes WHERE id = ?
        ''', (cafe_id,))
        
        conn.commit()
        conn.close()
        
db_restaurant = DatabaseManager(RESTAURANT_DB_PATH)
db_cafe = DatabaseManager(CAFE_DB_PATH)