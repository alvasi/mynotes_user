CREATE TABLE notes_user_2 (
    id SERIAL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    dob DATE,
    userid varchar(100) NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);

SELECT * FROM notes_user_2;