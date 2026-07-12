import sqlite3
from src.config.settings import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.initialize_database()
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
    def check_slot_available(self, date: str, time: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE date=? AND time=?
            """,
            (date, time),
        )
        result = cursor.fetchone()
        conn.close()
        return result is None
    def reserve_slot(self, date: str, time: str, email: str) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO appointments(date, time, email)
                VALUES (?, ?, ?)
                """,
                (date, time, email)
            )    
            conn.commit()
            return True    
        except sqlite3.Error:
            return False  
        finally:
            conn.close()
    def get_all_bookings(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        bookings = cursor.fetchall()
        conn.close()
        return bookings

db = DatabaseManager()