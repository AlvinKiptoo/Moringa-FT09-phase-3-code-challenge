from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        
        self._id = id
        self._name = name
        self._category = category

        if self._id is None:
            self._id = self._save_to_db()  # Save to DB and get the new ID

    def _save_to_db(self):
        """Saves a new Magazine to the database and returns its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", 
            (self._name, self._category)
        )
        conn.commit()
        magazine_id = cursor.lastrowid  # Get the auto-generated ID
        conn.close()
        return magazine_id

    @property
    def id(self):
        """Getter for the magazine's ID."""
        return self._id

    @property
    def name(self):
        """Getter for the magazine's name."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for the magazine's name."""
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
        self._update_db("name", value)

    @property
    def category(self):
        """Getter for the magazine's category."""
        return self._category

    @category.setter
    def category(self, value):
        """Setter for the magazine's category."""
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
        self._update_db("category", value)

    def _update_db(self, column, value):
        """Updates a specific column in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE magazines SET {column} = ? WHERE id = ?", 
            (value, self._id)
        )
        conn.commit()
        conn.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def articles(self):
        """Returns all articles associated with this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        """Returns all authors who have written for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?
        """, (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors

    def article_titles(self):
        """Returns a list of all article titles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title 
            FROM articles 
            WHERE magazine_id = ?
        """, (self._id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        """Returns authors who have written more than 2 articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        """, (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None
