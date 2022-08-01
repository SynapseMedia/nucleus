-- Tables schema definition for watchit cache storage.
-- ref: https://www.sqlstyle.guide/
-- Schema table definition for movies.
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    -- imdb code is adopted from IMB movies site to handle an alpha-numeric id
    imdb_code TEXT KEY DESC,
    title TEXT KEY DESC,
    group_name TEXT KEY,
    -- creator key itself is a public key from blockchain network
    creator_key TEXT,
    mpa_rating TEXT,
    rating REAL,
    runtime REAL,
    release_year INTEGER,
    synopsis TEXT,
    speech_language TEXT,
    trailer_code TEXT,
    date_uploaded REAL
);
-- Schema for movies_movie_genre join table.
CREATE TABLE IF NOT EXISTS movies_movie_genre (
    genre_id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    FOREIGN_KEY(movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
    FOREIGN_KEY(genre_id) REFERENCES movies_genres (genre_id) ON DELETE CASCADE
);
-- Schema table definition for movies_genres.
CREATE TABLE IF NOT EXISTS movies_genres (
    genre_id INTEGER PRIMARY KEY,
    genre KEY TEXT NOT NULL,
);
-- Schema table definition for movies_resources.
CREATE TABLE IF NOT EXISTS movies_resources (
    movie_id INTEGER NOT NULL,
    -- sqlite does not support ENUM types, so should be handled in code. eg: video=1, images=2.
    type INTEGER,
    -- Where the resource is stored?
    route TEXT,
    FOREIGN_KEY(movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE
);
-- Each group CAN have differents imdb_code entries.
CREATE UNIQUE INDEX IF NOT EXISTS idx_imdb_code ON movies(imdb_code, group_name);