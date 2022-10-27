import pytest
import sqlite3

@pytest.fixture(scope="session")
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            -- imdb code is adopted from IMB movies site to handle an alpha-numeric id
            imdb_code TEXT KEY DESC,
            title TEXT KEY DESC,
            -- creator key itself is a public key from blockchain network
            creator_key TEXT,
            mpa_rating TEXT,
            rating REAL,
            runtime REAL,
            release_year INTEGER,
            synopsis TEXT,
            genres TEXT,
            speech_language TEXT,
            trailer_link TEXT,
            publish_date REAL
        );
        """
    )
    
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            -- sqlite does not support ENUM types, so should be handled in code. eg: video=1, images=2.
            type INTEGER,
            -- Where the resource is stored?
            route TEXT,
            fk_movie FOREIGN_KEY movie_id REFERENCES movies (movie_id) ON DELETE CASCADE
        );
        """
    )

    yield conn

