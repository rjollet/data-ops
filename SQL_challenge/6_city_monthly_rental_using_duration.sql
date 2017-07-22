SELECT
  Cars.city,
  EXTRACT( YEAR FROM Rentals.starts_at) AS year,
  EXTRACT( MONTH FROM Rentals.starts_at) AS month,
  MAX(Rentals.duration) as total
FROM Rentals LEFT JOIN Cars ON Rentals.car_id = Cars.id
GROUP BY Cars.city, year, month
LIMIT 10;
