import pandas as pd
import numpy as np

from label import LABEL

lab_to_v = dict(LABEL)
v_to_lab = {l[1]: l[0] for l in LABEL}


input_cars_csv_path = '../data/cars.csv'
input_rentals_csv_path = '../data/rentals.csv'
input_unavailabilities_csv_path = '../data/unavailabilities.csv'

output_cars_half_day_state_csv_path = 'output/cars_half_day_state.csv'


#load csv
print('load csv')
cars_df = pd.read_csv(input_cars_csv_path, index_col='id', parse_dates=['created_at'])
rentals_df = pd.read_csv(input_rentals_csv_path, index_col='id', parse_dates=['starts_at', 'ends_at'])
unavailabilities_df =  pd.read_csv(input_unavailabilities_csv_path, index_col='id', parse_dates=['starts_at', 'ends_at'])

# (level 2) propagate last valid created_at forward to next valid created_at
cars_df.created_at.fillna(method='pad', inplace=True)

# get the list of halfdays for 2015
print('initialise car availabilities')
year_2015 = pd.date_range('2015-1-1 00:00:00', '2015-12-31 12:00:00', freq='12H').values

def initialise_car_availabilities(start, mask):
    return np.where((mask < start), lab_to_v['unavailable'], lab_to_v['available'])

def mask_period(start, end, mask):
    return ((mask > start) & (mask < end))

cars_df['availabilities'] = [initialise_car_availabilities(start, year_2015) for start in cars_df.created_at.values]

print('check rentals schedule')
cars_df['rented'] = rentals_df.groupby('car_id').apply(
    lambda car: np.vstack([
        mask_period(start, end, year_2015)
        for start, end in zip(car.starts_at.values, car.ends_at.values)
    ]).any(axis=0)
)

print('check unavailabilities schedule')
cars_df['unavailable'] = unavailabilities_df.groupby('car_id').apply(
    lambda car: np.vstack([
        mask_period(start, end, year_2015)
        for start, end in zip(car.starts_at.values, car.ends_at.values)
    ]).any(axis=0)
)

print('update availabilities')
def merge_availabilities(availabilities, rented, unavailable):
    if not np.any(pd.isnull(rented)):
        availabilities[rented] = lab_to_v['rented']
    if not np.any(pd.isnull(unavailable)):
        availabilities[unavailable] = lab_to_v['unavailable']
    return availabilities

cars_df.availabilities = [
    merge_availabilities(availabilities, rented, unavailable)
    for availabilities, rented, unavailable in zip(cars_df.availabilities, cars_df.rented, cars_df.unavailable)
]

print('save csv to ' + output_cars_half_day_state_csv_path)
cars_state_df = pd.DataFrame(np.vstack(cars_df.availabilities.values), columns=year_2015, index=cars_df.index).T \
  .to_csv(output_cars_half_day_state_csv_path)
print('done')
