DROP TABLE IF EXISTS BDAYS;
CREATE TABLE IF NOT EXISTS BDAYS
         (ID INTEGER PRIMARY KEY NOT NULL,
         USERNAME         TEXT  NOT NULL UNIQUE,
         DATE                         TEXT  NOT NULL);
