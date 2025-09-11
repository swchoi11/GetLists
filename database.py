import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_name="cafelist.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
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

    def delete_cafe(self, cafe_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM cafes WHERE id = ?
        ''', (cafe_id,))
        
        conn.commit()
        conn.close()
    
db_manager = DatabaseManager()
