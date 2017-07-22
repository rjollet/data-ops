WITH cars_rented_gth_3_monthly AS (
  SELECT
    car_id,
    EXTRACT(YEAR FROM starts_at) AS year,
    EXTRACT(MONTH FROM starts_at) AS month
  FROM Rentals
  GROUP BY car_id, year, month
  HAVING COUNT(DISTINCT id) >= 3
)

SELECT
  year,
  month,
  COUNT(DISTINCT car_id)
FROM cars_rented_gth_3_monthly
GROUP BY year, month;
