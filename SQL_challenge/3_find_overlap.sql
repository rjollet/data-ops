SELECT
  COUNT(*) as nb_overlaps
FROM Rentals CROSS JOIN Unavailabilities
WHERE Rentals.car_id = Unavailabilities.car_id
AND (Rentals.starts_at, Rentals.ends_at) OVERLAPS (Unavailabilities.starts_at, Unavailabilities.ends_at);
