ALTER TABLE Rentals DROP COLUMN IF EXISTS duration;
ALTER TABLE Rentals ADD COLUMN duration int;

UPDATE Rentals 
SET duration = trunc(((EXTRACT( epoch FROM ends_at - starts_at) / (60*60*12)) - 1) / 2) + 1  ;
