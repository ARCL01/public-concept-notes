PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS uploads(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    size INTEGER NULL
);