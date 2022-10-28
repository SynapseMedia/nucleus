PRAGMA foreign_keys = ON;
-- Tables schema definition for watchit cache storage.
-- ref: https://www.sqlstyle.guide/
-- Schema table definition for movies.
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- imdb code is adopted from IMB movies site to handle an alpha-numeric id
    imdb_code TEXT KEY DESC,
    title TEXT KEY DESC,
    -- creator key itself is a public key from blockchain network
    genres TEXT,
    creator_key TEXT,
    mpa_rating TEXT,
    rating REAL,
    runtime REAL,
    release_year INTEGER,
    synopsis TEXT,
    speech_language TEXT,
    trailer_link TEXT,
    publish_date REAL
    resources TEXT
);