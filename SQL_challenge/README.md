# SQL challenge

Thanks to the provided CSV files, you will need to answer the following questions with SQL queries. We recommend that you use PostgreSQL as you may want to use window functions.

**First in order to install the posgres database you can used the docker-compose.yml**

```
docker-compose up
```

```
psql -h localhost -p 5432 -U squad --password
```

1. Explain how you create tables and load data into these tables

  **You can find the answer in 1_load_tables.sql**
  ```
  psql -h localhost -p 5432 -U squad --password < 1_load_tables.sql
  ```

1. According to you, in which timezone rentals and unavailabilities datetimes are stored in?

  **Use the default timezone that has been set as UTC in 1_load_tables.sql**

1. Verify that you don't have any overlap between unavailabilities and rentals for each car

  ```
  psql -h localhost -p 5432 -U squad --password < 3_find_overlap.sql
  ```

  **This SQL scipts (3_find_overlap.sql) returns the number of overlaps, it returns 0 so there is no overlaps.**

1. Find the top 10 cities with the highest number of cars. Only display 10 rows

  ```
  psql -h localhost -p 5432 -U squad --password < 4_top_10_city_nb_cars.sql
  ```
  ```
      city     | nb_cars
  -------------+---------
   Paris       |   14964
   Lyon        |    3679
   Montpellier |    2542
   Toulouse    |    2257
   Nice        |    2248
   Marseille   |    2171
   Bordeaux    |    2049
   Lille       |    1363
   Rennes      |    1354
   Ajaccio     |    1138
  (10 rows)
  ```

1. For each rental, create a new column duration and compute it as explained. The duration is based on the number of half-days for a rental. A rental starting at 2017-06-01 00:00:00 and ending on 2017-06-02 12:00:00 spawns 3 half-days: [2017-06-01 AM, 2016-06-01 PM, 2017-06-02 AM]. The first 3 half-days count for a duration of 1, and then we need 2 more half-days to increase the duration (a duration of 2 can be made of 4 or 5 half-days).

  **The SQL script is in 5_add_rental_duration.sql drops the column duration if already exists, add the column and update the column to add the computed duration.

  to get the duration we get the number of second in the interval from starts_at to ends_at the we convert it in number of half day. we remove 1 half-days because the first period is 3 half day. then we divide by 2 and truncate in order to get the integer division. Finally we had one to get the duration value.**

  ```
  psql -h localhost -p 5432 -U squad --password < 5_add_rental_duration.sql
  ```

1. Find the total number of rental days (using the duration column) for each city, for each month. You can attribute a rental to a month thanks to its starts_at column. Can you explain which bias we have with this? What would be a better way to count the number of rental days?

    **Join Rentals and Cars On Rentals using Rentals.car_id = Cars.id, aggregate city year and month of starts_at and SUM duration columns.
    There are several biases:
    - duration is not exactly the number of days.
    - if the rental starts_at at a month but ends_at another month the it will only count for the starts_at month.

    A better way would be to from starts_at and ends_at to get the number of day in this interval per month.**

  ```
  psql -h localhost -p 5432 -U squad --password < 6_city_monthly_rental_using_duration.sql
  ```
  ```
  city    | year | month | total
  -----------+------+-------+-------
  Abbeville | 2014 |    12 |     6
  Abbeville | 2015 |     1 |    15
  Abbeville | 2015 |     2 |     9
  Abbeville | 2015 |     3 |    15
  Abbeville | 2015 |     4 |    15
  Abbeville | 2015 |     5 |    10
  Abbeville | 2015 |     6 |    15
  Abbeville | 2015 |     7 |    15
  Abbeville | 2015 |     8 |    15
  Abbeville | 2015 |     9 |    11
  ```

1. We now want to fix the NULL created_at for cars. For each car with a NULL created_at, we will consider that they were created on the same date as the previous car (ie. the car with the closest id before with a non null created_at). Assume that cars can be more than 1 ID apart.

  ```
  psql -h localhost -p 5432 -U squad --password < 7_fix_NULL_Cars_created_at.sql
  ```

  **With a table prev that is a lag 1 of the created_at UPDATE the Cars that have the create_at NULL with the prev created_at.**

1. For each month, find how many cars reach their 3rd rental. Use the starts_at to determine the month to attribute.

  **with a sub-query that select the car that have been rented at least 3 time in a month then cont the number of car per month.**

  ```
  psql -h localhost -p 5432 -U squad --password < 8_monthy_cars_reach_3_rentals.sql
  ```
  ```
  year | month | count
  ------+-------+-------
  2015 |     1 |  6782
  2015 |     2 |  9755
  2015 |     3 | 13617
  2015 |     4 | 20723
  2015 |     5 | 22653
  2015 |     6 | 21948
  2015 |     7 | 58563
  2015 |     8 | 65917
  2015 |     9 | 30281
  2015 |    10 | 34784
  2015 |    11 | 19647
  2015 |    12 | 43199
  (12 rows)
  ```
