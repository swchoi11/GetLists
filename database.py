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
    
db_manager = DatabaseManager()
