
# Surf's Up!: Hawaii Weather Analysis
This project was done using Numpy, Pandas, MatPlotLib, and Seaborn for analysis,
SQLAlchemy serving to connect to a SQLite database I created from CSVs I 
cleaned, and Flask to generate a mini-API.

This README comprises the Weather Analysis portion of the project. For other aspects, please see the following files:
- data_engineering.ipynb : This file contains the code used to clean the provided CSV datasets.
- database_engineering.ipynb : This file contains the code used to create a SQLite database from the cleaned CSVs.
- app.py : This file contains code for a Flask API based on the datasets I used.
- aux.py : This file contains some functions I coded that I decided to separate out into a module to make my code more readable.

Datasets were provided by Trilogy Education Services (&copy; 2017).


```python
# ----------------------------------------------------------------------
# Step 1: Import all necessary modules for analysis
# ----------------------------------------------------------------------
# import modules for analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import aux_func as aux
```


```python
# ----------------------------------------------------------------------
# Step 2: Set up db connection and session
# ----------------------------------------------------------------------
# set up sqlalchemy engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///hawaii.sqlite')
conn = engine.connect()

# set up sqlalchemy base
from sqlalchemy.ext.automap import automap_base
Base = automap_base()
Base.prepare(engine, reflect=True)

# map classes
Station = Base.classes.stations
Measurement = Base.classes.measurements

# set up session
from sqlalchemy.orm import Session
session = Session(engine)
```


```python
# ----------------------------------------------------------------------
# Step 3: Set overall chart appearances
# ----------------------------------------------------------------------
# set chart style
palette = sns.husl_palette(10)
sns.set(style="darkgrid", palette=palette)

# create dictionary with all color values
hex_codes = palette.as_hex()
palette_dict = {'light coral':hex_codes[0], 
                'orange':hex_codes[1], 
                'goldenrod':hex_codes[2], 
                'olive green':hex_codes[3], 
                'emerald':hex_codes[4], 
                'teal':hex_codes[5], 
                'cerulean':hex_codes[6], 
                'steel blue':hex_codes[7], 
                'lilac':hex_codes[8], 
                'pink':hex_codes[9]}

# show color palette
sns.palplot(palette)
```


![png](output_3_0.png)


## Precipitation Analysis
Between 8/24/2016 and 8/23/2017, Hawaii appears to have recorded observations of some level of precipitation almost every single day. However, it's unclear if precipitation includes only rain or if it includes precipitation like dew.

Across the 2,015 recorded observations, the maximum amount of precipitation recorded was 6.7 inches, but the mean was 0.18 inches.


```python
# ----------------------------------------------------------------------
# Step 4: Plot 12 months of precipitation data using using DF.plot.
#         Since didn't have data past August 2017, set end date at the 
#         last date where data was available
# ----------------------------------------------------------------------
# create variables for last year's date in string format and query (for readability)
last_year_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
query = f'SELECT date, precipitation FROM measurements WHERE date > "{last_year_start}"'

# read query into dataframe
last_year_prec_df = pd.read_sql(query, engine)
```


```python
# set style
plt.rcParams["figure.figsize"] = [16,8]

# plot the dataframe
last_year_grouped_df = last_year_prec_df.groupby('date').mean().reset_index()
last_year_grouped_df.plot.bar(color=palette_dict['cerulean'])
plt.title('Average Recorded Daily Precipitation (in Inches) in Hawaii from 8/24/16-8/23/17', 
          size=16)

# set proper labels
plt.xticks([x*30 for x in np.arange(13)],
           [list(last_year_grouped_df['date'])[x*30] for x in np.arange(13)],
           rotation=45, horizontalalignment='right')
plt.show()
```


![png](output_6_0.png)



```python
# display summary statistics
summary_stats_df = (last_year_prec_df.describe().reset_index().
                    rename(columns={'index':'stat'}).copy())
summary_stats_df['precipitation'] = summary_stats_df['precipitation'].round(2)
summary_stats_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>stat</th>
      <th>precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>count</td>
      <td>2015.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>mean</td>
      <td>0.18</td>
    </tr>
    <tr>
      <th>2</th>
      <td>std</td>
      <td>0.46</td>
    </tr>
    <tr>
      <th>3</th>
      <td>min</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>25%</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>50%</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>6</th>
      <td>75%</td>
      <td>0.13</td>
    </tr>
    <tr>
      <th>7</th>
      <td>max</td>
      <td>6.70</td>
    </tr>
  </tbody>
</table>
</div>



## Station Analysis
In this section, I parse through the weather stations that were available as part of the dataset.

There are a total of 9 weather stations in Hawaii, according to the dataset. Of those, the station with the highest observation count is USC00519281 WAIHEE 837.5 with a total of 2,772 observation across the dataset.


```python
# ----------------------------------------------------------------------
# Step 6: Calculate the total number of stations
# ----------------------------------------------------------------------
total_stations = pd.read_sql('SELECT COUNT(*) AS "Total Stations" FROM stations', 
                             engine)['Total Stations'][0]
print(f"There are {total_stations} weather stations in Hawaii.")
```

    There are 9 weather stations in Hawaii.



```python
# ----------------------------------------------------------------------
# Step 7: Find the most active stations
# ----------------------------------------------------------------------
# pull the stations and observation counts in descending order
query = 'SELECT m.station, s.name, COUNT(m.temp) AS "Count Observations" \
         FROM measurements m JOIN stations s ON s.station = m.station \
         GROUP BY m.station ORDER BY COUNT(m.temp) DESC'
station_obs_count_desc = pd.read_sql(query,engine)

# display station with highest observation count and df of all stations
highest_obs = f'{station_obs_count_desc["station"][0]} {station_obs_count_desc["name"][0]}'
print(f'The station with the highest observation count is {highest_obs}.')
station_obs_count_desc
```

    The station with the highest observation count is USC00519281 WAIHEE 837.5.





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>Count Observations</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519281</td>
      <td>WAIHEE 837.5</td>
      <td>2772</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1</td>
      <td>2696</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2</td>
      <td>2685</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM</td>
      <td>2572</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00516128</td>
      <td>MANOA LYON ARBO 785.2</td>
      <td>2484</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9</td>
      <td>1937</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00511918</td>
      <td>HONOLULU OBSERVATORY 702.2</td>
      <td>1932</td>
    </tr>
    <tr>
      <th>7</th>
      <td>USC00517948</td>
      <td>PEARL CITY</td>
      <td>683</td>
    </tr>
    <tr>
      <th>8</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3</td>
      <td>342</td>
    </tr>
  </tbody>
</table>
</div>



## Temperature Analysis
### Part 1: Temperature Histogram (2016-2017)
Between 8/24/2016 and 8/23/2017, the majority of recorded temperature observations were between 72.5-77.5&deg;F with the average recorded temperature observation somewhere around 75&deg;F.


```python
# ----------------------------------------------------------------------
# Step 8: Graph 12 months worth of temperature data from the station with
#       the most observations.
# ----------------------------------------------------------------------
# read query into dataframe
query = f'SELECT date, station, temp FROM measurements \
          WHERE date > "{last_year_start}" AND \
          station = "{station_obs_count_desc["station"][0]}"'
last_year_temp_df = pd.read_sql(query, engine)['temp']

# plot histogram
#plt.hist(x=last_year_temp_df, bins=12, histtype='bar')
sns.distplot(last_year_temp_df, bins=12, color=palette_dict['light coral'],
            hist_kws={'color':palette_dict['orange']})
plt.title(f"Observed Temperature Distribution at Weather Station {highest_obs} between 8/24/16-8/23/17",
         size=16)
plt.xlabel('Temperature (Fahrenheit)', size=13)
plt.ylabel('Frequency', size=13)
plt.show()
```


![png](output_12_0.png)


### Part Two: Temperature Analysis for Trip to Hawaii
Part of this assignment was to calculate the likely temperature for a theoretical trip to Hawaii for myself. The dates I selected for my trip were: 6/28/2018-07/04/2018.

Results can be seen in the chart below. Barring any unusual weather patterns, I can reasonably expect the average temperature for my trip to be 75&deg;F. As you can see from the error bars, the recorded temperature has reached a minimum of 67&deg;F and a maximum of 82&deg;F, so it seems reasonable to prepare for temperatures to be in the 70s for the majority of my trip.

Please note: The error bars on the chart are slightly off (by 1-2&deg;F) due to a known MatPlotLib bug. For exact min/max temperatures, see the dataframe below the chart.


```python
# ----------------------------------------------------------------------
# Step 9: Calculate the likely average, min, and max for my theoretical 
#         trip
# ----------------------------------------------------------------------# 
# start and end dates for my trip
start_date = dt.date(2018, 6, 28)
end_date = dt.date(2018, 7, 4)

# min and max for data set
min_date = dt.date(2010, 1, 1)
max_date = dt.date(2017, 8, 23)

# set length of previous month
prev_month_length = 30

# get num days and years in data set
num_days = (end_date - start_date).days
num_years = int(round((max_date - min_date).days/365,0))

# create list of all dates to be searched
search_dates = aux.get_search_list(start_date, end_date, min_date, max_date, 
                                prev_month_length, num_days, num_years)

# using list of dates, get avg temp, min temp, max temp in a dataframe
trip_temp_df = aux.calc_temps(num_days, num_years, search_dates, engine)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month/day</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>avg/min diff</th>
      <th>avg/max diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>07-04</td>
      <td>76.574468</td>
      <td>70</td>
      <td>81</td>
      <td>6.574468</td>
      <td>4.425532</td>
    </tr>
    <tr>
      <th>1</th>
      <td>07-03</td>
      <td>74.808511</td>
      <td>68</td>
      <td>82</td>
      <td>6.808511</td>
      <td>7.191489</td>
    </tr>
    <tr>
      <th>2</th>
      <td>07-02</td>
      <td>75.166667</td>
      <td>68</td>
      <td>82</td>
      <td>7.166667</td>
      <td>6.833333</td>
    </tr>
    <tr>
      <th>3</th>
      <td>07-01</td>
      <td>74.958333</td>
      <td>68</td>
      <td>81</td>
      <td>6.958333</td>
      <td>6.041667</td>
    </tr>
    <tr>
      <th>4</th>
      <td>06-30</td>
      <td>75.380000</td>
      <td>67</td>
      <td>81</td>
      <td>8.380000</td>
      <td>5.620000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>06-29</td>
      <td>74.705882</td>
      <td>67</td>
      <td>80</td>
      <td>7.705882</td>
      <td>5.294118</td>
    </tr>
    <tr>
      <th>6</th>
      <td>06-28</td>
      <td>74.770833</td>
      <td>69</td>
      <td>80</td>
      <td>5.770833</td>
      <td>5.229167</td>
    </tr>
  </tbody>
</table>
</div>




```python
# generate list of error pairs for plotting error bars
yerr_line_list=[]
[yerr_line_list.append((trip_temp_df['avg/min diff'][i] + 
                        trip_temp_df['avg/max diff'][i])) for i in np.arange(num_days+1)]

# plot error data
plt.bar(x=trip_temp_df['month/day'], 
        height=trip_temp_df['avg_temp'], color=hex_codes)
plt.errorbar(x=trip_temp_df['month/day'],
             y=trip_temp_df['max_temp'],
             yerr=yerr_line_list, uplims=True,
             ecolor='black', fmt='none')
plt.title("Expected Temperatures for 6/28-7/4/2018 (Using 2010-17 Data)", 
          size=16)
plt.ylabel('Average Temperature (Fahrenheit)', size=13)
plt.xlabel('Day', size=13)
plt.ylim(40,90)
plt.show()
trip_temp_df
```


![png](output_15_0.png)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month/day</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>avg/min diff</th>
      <th>avg/max diff</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>07-04</td>
      <td>76.574468</td>
      <td>70</td>
      <td>81</td>
      <td>6.574468</td>
      <td>4.425532</td>
    </tr>
    <tr>
      <th>1</th>
      <td>07-03</td>
      <td>74.808511</td>
      <td>68</td>
      <td>82</td>
      <td>6.808511</td>
      <td>7.191489</td>
    </tr>
    <tr>
      <th>2</th>
      <td>07-02</td>
      <td>75.166667</td>
      <td>68</td>
      <td>82</td>
      <td>7.166667</td>
      <td>6.833333</td>
    </tr>
    <tr>
      <th>3</th>
      <td>07-01</td>
      <td>74.958333</td>
      <td>68</td>
      <td>81</td>
      <td>6.958333</td>
      <td>6.041667</td>
    </tr>
    <tr>
      <th>4</th>
      <td>06-30</td>
      <td>75.380000</td>
      <td>67</td>
      <td>81</td>
      <td>8.380000</td>
      <td>5.620000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>06-29</td>
      <td>74.705882</td>
      <td>67</td>
      <td>80</td>
      <td>7.705882</td>
      <td>5.294118</td>
    </tr>
    <tr>
      <th>6</th>
      <td>06-28</td>
      <td>74.770833</td>
      <td>69</td>
      <td>80</td>
      <td>5.770833</td>
      <td>5.229167</td>
    </tr>
  </tbody>
</table>
</div>


