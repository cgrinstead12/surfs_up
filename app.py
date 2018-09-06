import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

# Getting a list of dates for the last 12 months
base_date = dt.datetime.strptime("2017-08-23", "%Y-%m-%d")
ndays = 365
date_list = [base_date - dt.timedelta(days=x) for x in range(0, ndays)]

# Converting them to a list of strings
str_dates = []
for date in date_list:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)

@app.route("/")

def welcome():
	return(
       f"Welcome to the home page!<br/>"
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/start_date<br/>"
       f"/api/v1.0/start_date/end_date<br/>"
       f"Please enter dates in 'YYYY-MM-DD' format"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))
    
    prcp_data = []
    for day in results:
        prcp_dict = {}
        prcp_dict[day.date] = day.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query temperatures
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))

    temp_data = []
    for day in results:
        temp_dict = {}
        temp_dict[day.date] = day.tobs
        temp_data.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def temperature_s(start):
    # Set start and end dates for date range
    startDate = dt.datetime.strptime(start, "%Y-%m-%d")
    endDate = dt.datetime.strptime("2017-08-23", "%Y-%m-%d")

    query = session.query(Measurement.tobs).filter(Measurement.date>=startDate, Measurement.date<=endDate).all()
    temperatures = [temp[0] for temp in query]
    avg_temp = np.mean(temperatures)
    lowest_temp = min(temperatures)
    highest_temp = max(temperatures)

    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Average Temperature"] = avg_temp
    temp_dict["Minimum Temperature"] = lowest_temp
    temp_dict["Maximum Temperature"] = highest_temp

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):
    # Set start and end dates for date range
    startDate = dt.datetime.strptime(start, "%Y-%m-%d")
    endDate = dt.datetime.strptime(end, "%Y-%m-%d")

    query = session.query(Measurement.tobs).filter(Measurement.date>=startDate, Measurement.date<=endDate).all()
    temperatures = [temp[0] for temp in query]
    avg_temp = np.mean(temperatures)
    lowest_temp = min(temperatures)
    highest_temp = max(temperatures)

    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Average Temperature"] = avg_temp
    temp_dict["Minimum Temperature"] = lowest_temp
    temp_dict["Maximum Temperature"] = highest_temp

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
