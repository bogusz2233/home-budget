CREATE TABLE IF NOT EXISTS property ( 
    id_p INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- format: YYYY-MM
    year_month_of_creation TEXT NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL
);