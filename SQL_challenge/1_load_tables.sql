DROP TABLE IF EXISTS Cars, Rentals, Unavailabilities;

SET timezone TO 'UTC';

CREATE TABLE Cars (
  id bigserial NOT NULL PRIMARY KEY,
  city varchar,
  created_at date NULL
);

CREATE TABLE Rentals (
  id bigserial NOT NULL PRIMARY KEY,
  car_id bigserial REFERENCES Cars(id),
  starts_at timestamp,
  ends_at timestamp
);

CREATE TABLE Unavailabilities (
  id bigserial NOT NULL PRIMARY KEY,
  car_id bigserial REFERENCES Cars(id),
  starts_at timestamp,
  ends_at timestamp
);


COPY Cars FROM '/data_csv/cars.csv' DELIMITER ',' CSV HEADER NULL as 'NULL';
COPY Rentals FROM '/data_csv/rentals.csv' DELIMITER ',' CSV HEADER NULL as 'NULL';
COPY Unavailabilities FROM '/data_csv/unavailabilities.csv' DELIMITER ',' CSV HEADER NULL as 'NULL';
