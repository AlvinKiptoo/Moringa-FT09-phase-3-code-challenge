import sqlite3
from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        
        self._id = id
        self._name = name

        if self._id is None:
            self._id = self._save_to_db()

    def _save_to_db(self):
        """Saves a new Author to the database and returns its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        conn.commit()
        author_id = cursor.lastrowid  # Get the auto-generated ID
        conn.close()
        return author_id

    @property
    def id(self):
        """Getter for the author's ID."""
        return self._id

    @property
    def name(self):
        """Getter for the author's name."""
        return self._name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    def articles(self):
        """Returns all articles associated with this author."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        """Returns all magazines associated with this author."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines
