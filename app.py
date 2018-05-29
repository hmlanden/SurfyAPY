# ----------------------------------------------------------------------
# Step 1: Import all necessary modules and create Flask app
# ---------------------------------------------------------------------- 
from flask import Flask, jsonify, render_template
import pandas as pd
import datetime as dt

# create app
app = Flask(__name__)

# ----------------------------------------------------------------------
# Step 3: Set up db connection and session
# ----------------------------------------------------------------------
# set up sqlalchemy engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///hawaii.sqlite')

# set up sqlalchemy base
from sqlalchemy.ext.automap import automap_base
Base = automap_base()
Base.prepare(engine, reflect=True)

# map classes
Station = Base.classes.stations
Measurement = Base.classes.measurements

# ----------------------------------------------------------------------
# Step 3: Create all required routes
# ---------------------------------------------------------------------- 
@app.route("/")
def welcome():
    return 'Welcome to the API!';


# dates and precipitation observations from the last year in the dataset
@app.route('/api/v1.0/precipitation')
def precipitation():
    last_year_start = (dt.date(2017,8,23) - dt.timedelta(days=365)).isoformat()
    query = (f'SELECT date, precipitation FROM measurements \
             WHERE date > "{last_year_start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    query = 'SELECT station, name FROM stations'
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list of Temperature Observations (tobs) for the previous year 
#@app.route('/api/v1.0/tobs')
#def tobs():
#    return "hi";

# json list of the min temp, avg temp, max temp where date = given start<=
@app.route('/api/v1.0/<start>')
def temps_startOnly(start):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
             AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
             FROM measurements WHERE date >= "{start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));

# json list: min temp, avg temp, max temp for dates between start/end inclusive
@app.route('/api/v1.0/<start>/<end>')
def temps_startAndEnd(start, end):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
             AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
             FROM measurements WHERE date >= "{start}" AND date <= "{end}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));  

# ----------------------------------------------------------------------
# Step 4: Define main
# ---------------------------------------------------------------------- 
if __name__ == "__main__":
    app.run(debug=True)