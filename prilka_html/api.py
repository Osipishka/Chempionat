import sqlite3
from typing import List, Dict, Any, Optional
from werkzeug.security import generate_password_hash, check_password_hash

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
        

    def login_user(self, login: str, password: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    ID as id,
                    Login as login,
                    Password as password,
                    Role as role
                FROM Users
                WHERE Login = ?
        """, (login))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None


    def reg_user(self, login: str, password: str) -> int:
        hashed = generate_password_hash(password)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (Login, Password) VALUES (?, ?)",
                (login, hashed)
            )
            conn.commit()
        return cursor.lastrowid

    def get_user(self, ) -> List[Dict[str, Any]]:
        """Получить получить пользователя"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                ID,
                Name as name,
                Fullname as fullname,
                Phone as phone,                           
                Birthday as birthday,
                Login as login,
                Password as password,     
                Role as role
            FROM Users
            ORDER BY ID
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    

    def get_games_paginated(self, page: int = 1, per_page: int = 5) -> Dict[str, Any]:
        """Получить игры с пагинацией"""
        offset = (page - 1) * per_page
    
        with self._get_connection() as conn:
            cursor = conn.cursor()
        
        # Получаем игры для текущей страницы
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
            LIMIT ? OFFSET ?
        """, (per_page, offset))
        
        games = [dict(row) for row in cursor.fetchall()]
        
        # Получаем общее количество игр
        cursor.execute("SELECT COUNT(*) as total FROM Games")
        total = cursor.fetchone()['total']
        
        return {
            'games': games,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

db_api = DatabaseAPI()