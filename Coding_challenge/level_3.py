import pandas as pd
import numpy as np

from label import LABEL
lab_to_v = dict(LABEL)

input_cars_csv_path = '../data/cars.csv'
input_cars_half_day_state_csv_path = 'output/cars_half_day_state.csv'

output_city_weekly_occupation_rate_csv_path = 'output/city_weekly_occupation_rate.csv'

print('load cars')
cars_df = pd.read_csv(input_cars_csv_path, index_col='id', parse_dates=['created_at'])
print('load car state')
cars_state_df = pd.read_csv(
    input_cars_half_day_state_csv_path,
    index_col=0,
    parse_dates=[0],
    dtype=np.int,
    na_filter=False,
    low_memory=True,
    memory_map=True).T

#rename the index and change its type to int in order to do the join
cars_state_df.index.name = 'id'
cars_state_df.index = cars_state_df.index.map(np.int)

# ts is the list of time in the time series
ts = cars_state_df.columns

def occupacy_rate(availabilities, time_range = False):
    res = (availabilities == lab_to_v['rented']).sum(axis=0) / (availabilities != lab_to_v['unavailable']).sum(axis=0)
    return res

print('get the occupation rate')
#compute the half day occupation date
city_half_day_occupation_rate_series = cars_df.join(cars_state_df).groupby('city').apply(
    lambda city: occupacy_rate(city[ts])
).T

#add a column with the week number
city_half_day_occupation_rate_series['week'] = city_half_day_occupation_rate_series.index.week

# group by week in order to get the weekly average occupation rate per city
city_half_day_occupation_rate_series = city_half_day_occupation_rate_series.groupby('week').mean()
print('save to csv')
# save the csv with the weekly occupation rate per city
city_half_day_occupation_rate_series.to_csv(output_city_weekly_occupation_rate_csv_path)
print('done')
