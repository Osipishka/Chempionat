import sqlite3
from typing import List, Dict, Any, Optional

class DatabaseAPI:
    def __init__(self, db_path: str = 'Games.db'):
        self.db_path = db_path
    
    def _get_connection(self):
        """Создание подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return conn
    
    # GET методы для получения данных
    
    def get_all_games(self) -> List[Dict[str, Any]]:
        """Получить все игры из таблицы Games"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                ID,
                Img as image_url,
                Genre as genre,
                Developer as developer,
                Rating as rating,
                Cost as price
            FROM Games
            ORDER BY ID
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    
    # POST/PUT/DELETE методы (примеры)
    
    def create_user(self, name: str, email: str) -> int:
        """Создать нового пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            return cursor.lastrowid

# Создаем экземпляр API для использования
db_api = DatabaseAPI()