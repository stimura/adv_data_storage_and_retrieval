import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func, desc
from matplotlib.ticker import NullFormatter
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import seaborn as sns
from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Copy/Paste for HW

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date(YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date/end_date(YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of the dates and temperature observations from the last year."""
    # Query results
    prcp_date_list = session.query(Measurement.date).\
                     group_by(Measurement.date).\
                     order_by(desc(Measurement.date)).limit(365).all()

    prcp_list = session.query(Measurement.prcp).\
                group_by(Measurement.date).\
                order_by(desc(Measurement.date)).limit(365).all()

    # Create a dictionary
    all_prcps = {"date" : prcp_date_list, "prcp" : prcp_list}
    
    return jsonify(all_prcps)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations from the dataset."""
    # Query results
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns list of Temperature Observations (tobs) for the previous year."""
    # Query results
    results = session.query(Measurement.date, Measurement.tobs).\
           filter(Measurement.date >= '2016-08-24').\
           filter(Measurement.date <= '2017-08-23').\
           group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    # Create a dictionary
    tobs_date_list = []
    tobs_list = []
    
    for tob in range(len(results)):
        (tobs_date, tobs) = results[tob]
        tobs_date_list.append(tobs_date)
        tobs_list.append(tobs)

    tobs_dict = {"date" : tobs_date_list, "tobs" : tobs_list}

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Returns a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query results
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).\
           group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    temp_dates = []
    min_temp_list = []
    avg_temp_list = []
    max_temp_list = []

    for temp in range(len(results)):
        (date, min_temp, avg_temp, max_temp) = results[temp]
        temp_dates.append(date)
        min_temp_list.append(min_temp)
        avg_temp_list.append(avg_temp)
        max_temp_list.append(max_temp)

    start_date_raw_dict = {
    "date" : temp_dates,
    "min_temp" : min_temp_list,
    "avg_temp" : avg_temp_list,
    "max_temp" : max_temp_list
    }

    return jsonify(start_date_raw_dict)

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    """Returns a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query results
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).\
           filter(Measurement.date <= end).\
           group_by(Measurement.date).order_by(Measurement.date.desc()).all()

    temp_dates = []
    min_temp_list = []
    avg_temp_list = []
    max_temp_list = []

    for temp in range(len(results)):
        (date, min_temp, avg_temp, max_temp) = results[temp]
        temp_dates.append(date)
        min_temp_list.append(min_temp)
        avg_temp_list.append(avg_temp)
        max_temp_list.append(max_temp)

    dates_raw_dict = {
    "date" : temp_dates,
    "min_temp" : min_temp_list,
    "avg_temp" : avg_temp_list,
    "max_temp" : max_temp_list
    }

    return jsonify(dates_raw_dict)

if __name__ == "__main__":
    app.run(debug=True)
