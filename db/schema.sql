CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_code TEXT,
    date TEXT,
    hour INTEGER,
    pollutant TEXT,
    value REAL
);
