from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        if not isinstance(content, str):
            raise ValueError("Content must be a string")

        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

        if self._id is None:
            self._id = self._save_to_db()  # Save to DB and get the new ID

    def _save_to_db(self):
        """Saves a new Article to the database and returns its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", 
            (self._title, self._content, self._author_id, self._magazine_id)
        )
        conn.commit()
        article_id = cursor.lastrowid  # Get the auto-generated ID
        conn.close()
        return article_id

    @property
    def id(self):
        """Getter for the article's ID."""
        return self._id

    @property
    def title(self):
        """Getter for the article's title."""
        return self._title

    @property
    def content(self):
        """Getter for the article's content."""
        return self._content

    @property
    def author_id(self):
        """Getter for the article's author ID."""
        return self._author_id

    @property
    def magazine_id(self):
        """Getter for the article's magazine ID."""
        return self._magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    
    def author(self):
        """Returns the author of this article."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self._author_id,))
        author = cursor.fetchone()
        conn.close()
        return author

    def magazine(self):
        """Returns the magazine of this article."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine
