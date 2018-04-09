# ----------------------------------------------------------------------
# Auxilary functions for climate analysis
# ----------------------------------------------------------------------
def get_search_list(start_date, end_date, min_date, max_date, 
                    prev_month_length, num_days, num_years):
    """
    Takes in a start date, end date, the minimum date of the available 
    data, the maximum date of the available data, the length of the 
    month before, how long the trip is in days, and how many years are
    in the dataset.
    
    Returns a list of list of all trip dates across all available years 
    in the data, sectioned by matching days.
    """
    # import necessary modules
    import numpy as np
    import datetime as dt
    
    # create empty lists
    search_dates = []
    sorted_search_dates = []
    
    # iterate through dates and return complete list in dt format
    for i in np.arange(num_years):
        for j in np.arange(num_days + 1):
            if end_date.day - j <= 0:
                search_dates.append((dt.date(max_date.year - i, 
                                            end_date.month - 1,
                                            prev_month_length - (abs(end_date.day - j)))))
            else:
                search_dates.append((dt.date(max_date.year - i, 
                                            end_date.month,
                                            end_date.day - j)))
    
    # iterate through list and return list of lists with dt objects by day
    for i in np.arange(num_days + 1):
        temp_list = []
        for j in np.arange(num_years):
            if j == 0:
                temp_list.append(search_dates[i])
            else:
                temp_list.append(search_dates[i + (j * 7)])
        
        sorted_search_dates.append(temp_list)
    
    return sorted_search_dates;  





def calc_temps(num_days, num_years, search_dates, engine):
    """
    Take in number of days for the trip, number of years in the dataset,
    complete set of matching dates from the dataset, and the engine from
    the SQLAlchemy connection.
    
    Returns a dataframe with the average temperature, minimum temperature,
    maximum temperature, difference between avg and min, and difference
    between avg and max for each day.
    """
    # import necessary modules
    import numpy as np
    import pandas as pd
    
    # set up sqlalchemy engine
    from sqlalchemy import create_engine
    engine = engine

    # set up sqlalchemy base
    from sqlalchemy.ext.automap import automap_base
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # map classes
    Station = Base.classes.stations
    Measurement = Base.classes.measurements
    
    final_result_list = []
    dict_result_list = []

    # get list of dataframes where each date has a df with all needed data
    for i in np.arange(num_days + 1):
        temp_result_df = pd.DataFrame()
        for j in np.arange(num_years):
            query = f'SELECT date, temp AS "Temp" FROM measurements \
                      WHERE date = "{search_dates[i][j].strftime("%Y-%m-%d")}"'
            temp_result_df = temp_result_df.append((pd.read_sql(query, engine)),
                                                   ignore_index=True)
        
        final_result_list.append(temp_result_df)
    
    # iterate through each dataframe and get the min, max, etc
    for i in np.arange(num_days + 1):
        curr_df = final_result_list[i]
        curr_df['year'], curr_df['month'], curr_df['day'] = curr_df['date'].str.split('-', 2).str
        dict_result_list.append({'date':curr_df['date'][0],
                                 'month':curr_df['month'][0],
                                 'year':curr_df['year'][0],
                                 'min_temp':(curr_df.groupby('day').min()['Temp'][0]), 
                                 'max_temp':(curr_df.groupby('day').max()['Temp'][0]),
                                 'avg_temp':(curr_df.groupby('day').mean()['Temp'][0])})
    
    # create dataframe
    result_df= pd.DataFrame.from_records(dict_result_list, 
                                         columns=['date', 'avg_temp', 'max_temp', 'min_temp'])
    
    # clean dataframe
    result_df['year'], result_df['month/day'] = (result_df['date'].
                                                 str.split('-', 1).
                                                 str)
    result_df.drop(columns=['year','date'], inplace=True)
    result_df = result_df[['month/day', 'avg_temp', 'min_temp', 'max_temp']]
    
    # add column with difference between min, avg, and max
    result_df['avg/min diff'] = result_df['avg_temp'] - result_df['min_temp']
    result_df['avg/max diff'] = result_df['max_temp'] - result_df['avg_temp']
    
    return result_df;                                                      
                                                  

