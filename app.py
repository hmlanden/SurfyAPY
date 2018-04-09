# ----------------------------------------------------------------------
# Step 1: Import all necessary modules and create Flask app
# ---------------------------------------------------------------------- 
from flask import Flask, jsonify

# create app
app = Flask(__name__)

# ----------------------------------------------------------------------
# Step 3: Set up db connection and session
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

# ----------------------------------------------------------------------
# Step 3: Create all required routes
# ---------------------------------------------------------------------- 
# dates and temperature observations from the last year
@app.route('/api/v1.0/precipitation')

# json list of stations from the dataset.
@app.route('/api/v1.0/stations')

# json list of Temperature Observations (tobs) for the previous year 
@app.route('/api/v1.0/tobs')


# json list of the min temp, avg temp, max temp where date = given start<=
@app.route('/api/v1.0/<start>')

# json list: min temp, avg temp, max temp for dates between start/end inclusive
@app.route('/api/v1.0/<start>/<end>')


# ----------------------------------------------------------------------
# Step 4: Define main
# ---------------------------------------------------------------------- 
if __name__ == "__main__":
    app.run(debug=True)