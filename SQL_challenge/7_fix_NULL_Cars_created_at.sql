WITH prev AS (
  SELECT
    id,
    lag(created_at, 1) over(order by id ASC) AS created_at
  FROM Cars
  ORDER BY id
)

UPDATE Cars
SET created_at = prev.created_at FROM prev WHERE Cars.created_at IS NULL AND prev.id = Cars.id;
