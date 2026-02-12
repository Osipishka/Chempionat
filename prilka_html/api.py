import sqlite3
from typing import List, Dict, Any, Optional

class DatabaseAPI:
    def __init__(self, db_path: str = 'Games.db'):
        self.db_path = db_path
    
    def _get_connection(self):
        """Создание подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_all_games(self) -> List[Dict[str, Any]]:
        """Получить все игры из таблицы Games"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                ID,
                Title as title,
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
    
    def create_game(self, title: str, img: str, genre: str, dev: str, rating: int, cost: int) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Games (Title, Img, Genre, Developer, Rating, Cost) VALUES (?, ?, ?, ?, ?, ?)",
                (title, img, genre, dev, rating, cost)
            )
            conn.commit()
        return cursor.lastrowid

    def edit_game(self, game_id: int, title: str, img: str, genre: str, dev: str, rating: int, cost: int) -> bool:
        """Обновить игру по ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Games 
                SET Title = ?, 
                    Img = ?, 
                    Genre = ?, 
                    Developer = ?, 
                    Rating = ?, 
                    Cost = ?
            WHERE ID = ?
        """, (title, img, genre, dev, rating, cost, game_id))
        conn.commit()
        return cursor.rowcount > 0
    
    def delete_game(self, game_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Games WHERE ID = ?", (game_id,))
            conn.commit()
        return cursor.rowcount > 0


    def get_game_by_id(self, game_id: int) -> Optional[Dict[str, Any]]:
        """Получить игру по ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    ID,
                    Title as title,
                    Img as image_url,
                    Genre as genre,
                    Developer as developer,
                    Rating as rating,
                    Cost as price
                FROM Games 
                WHERE ID = ?
            """, (game_id,))
        

    def login_user(self, login: str, password: int) -> Optional[Dict[str, Any]]:

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    ID as id,
                    Login as login,
                    Password as password,
                    Role as role
                FROM Users
                WHERE Login = ? AND Password = ?
        """, (login, password))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None


    def reg_user(self, login: str, password: int) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (Login, Password) VALUES (?, ?)",
                (login, password)
            )
            conn.commit()
        return cursor.lastrowid

    def get_user(self) -> List[Dict[str, Any]]:
        """Получить получить пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                ID,
                Title as title,
                Img as image_url,
                Genre as genre,
                Developer as developer,
                Rating as rating,
                Cost as price
            FROM Users
            ORDER BY ID
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

db_api = DatabaseAPI()