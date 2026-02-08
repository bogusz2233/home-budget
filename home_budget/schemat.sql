CREATE TABLE IF NOT EXISTS property ( 
    id_p INTEGER PRIMARY KEY AUTOINCREMENT,

    creation_time TEXT NOT NULL,

    name TEXT NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL
);