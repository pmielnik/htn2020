/* htn2020 database schema file */

PRAGMA foreign_keys = ON;

CREATE TABLE companies(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE locations(
    id INTEGER PRIMARY KEY,
    latitude BIGINT NOT NULL,
    longitude BIGINT NOT NULL
);

CREATE TABLE events(
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    picture TEXT,
    company_id INTEGER,
    location_id INTEGER,

    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE event_attendance(
    user_id INTEGER,
    event_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);