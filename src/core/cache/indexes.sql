-- Each group CAN have differents imdb_code entries.
CREATE UNIQUE INDEX IF NOT EXISTS idx_imdb_code ON movies(imdb_code, group_name);