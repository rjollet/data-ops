SELECT
  city,
  COUNT(DISTINCT id) AS nb_cars
FROM Cars
GROUP BY city
ORDER BY nb_cars DESC
LIMIT 10;
