## Coding challenge
**General instructions**: For the different levels, you should use the provided CSV files and a dynamic language such as Python or Ruby. You should read the CSV files, do some processing as asked and then output back your results to a CSV file with the appropriate columns.

**Goal:**
 Provide the business intelligence team a report of the occupancy rate of the fleet per city.

The occupancy rate of a given half-day is defined as the number of rented cars / number of available or rented cars.

For a half-day T, a car is considered `available` by default. This default state can be changed to:
- `rented`: the car is booked over T
- `unavailable`: the owner has declared not wanting to rent over T. The car hence gets hidden from search results and cannot receive rental requests

Each unavailability is a period defined by a start datetime and an end datetime. The level of detail is a half-day (AM/PM).

Rentals also are periods defined by a start datetime and end datetime with a level of detail of a half-day.

Cars have a `created_at` date: they do not exist on the website before this date.

**Example of calendar:**

![Calendar](https://drivy-misc.s3.amazonaws.com/jobs/calendar.jpg "Calendar")

**For this challenge I use numpy and pandas please use the requirements.txt to install them if you need. (you can use virtualenv)**

### Level 1
Compute the state of each car for each half-day in 2015. A car state can be `available`, `rented` or `unavailable`.
As a simplification you can consider that the cars with a `NULL` `created_at` field were created in 2014.

**Level 1 and 2 are in level_1_2.py**

```
python3 level_1_2.py
```

### Level 2
Write a program that fixes the `NULL` `created_at` values and outputs a fixed version of the cars CSV.
For each car with a `NULL` `created_at`, we will consider that they were created on the same date as the previous car (ie. the car with the previous `id`).
Don't forget to recompute the state of each car for each half-day in 2015.

**This function is native with pandas so I did it with the level 1**

```python3
cars_df.created_at.fillna(method='pad', inplace=True)
```

### Level 3
Compute the occupancy rate per week per city.

**Level 3 is in level_3.py**

```
python3 level_3.py
```

### Level 4
We now have the data needed by the business intelligence team and would like to automate a weekly reporting. Describe in a few lines how you would automate calculations and automatically send an extract every week.

1. extract the rentals and rental that have an ends_at that is after the today - 7 days
2. compute the cars state for the last 7 days (14 half days)
3. aggregate per city and get the weekly average occupation rate.

I would keep the last week state and update it every day by adding the today care state.

If the weekly reporting is to see the trend of the occupation rate of the past and future week. I will precompute the past week occupation rate and save them in a file of a db and compute daily the provisory occupation rate for the coming week.
