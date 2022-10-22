import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, engine_from_config, func

from flask import Flask, jsonify
import datetime as dt


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = base.classes.measurement
print(Measurement)
# # Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0//api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# for precipitation
# Convert the query results from your precipitation analysis
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    Session = Session(engine)

    recent_date = Session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    date_string = str(recent_date[0])
    # convert to string first
    date_format = dt.datetime.strptime(recent_date[0], "%Y-%m-%d")
    date_query = dt.date(int(date_format.strftime("%Y")), int(date_format.strftime("%m")), int(date_format.strftime("%d"))) - dt.timedelta(days=365)

    precip_score = Session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_query).all()

    Session.close()

    precipitation_list = []
    for precip in precip_score:
        precipitation_list[precip[0]] = precip[1]
    return jsonify(precipitation_list)

# for stations
# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    Session = Session(engine)
    station_count = Session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    Session.close()
    station_list = []
    for station in station_count:
        station_list.append([station[0], station[1]])
    return jsonify(station_list)

# for tobs
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def observations():
    Session = Session(engine)
    recent_date = Session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    date_string = str(recent_date[0])
    # convert to string first
    date_format = dt.datetime.strptime(recent_date[0], "%Y-%m-%d")
    date_query = dt.date(int(date_format.strftime("%Y")), int(date_format.strftime("%m")), int(date_format.strftime("%d"))) - dt.timedelta(days=365)

    precip_score = Session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_query).all()
    most_active_station = Session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    observations_list = []
    for observation in most_active_station:
        observations_list.append([observation[0], observation[1]])
    return jsonify(observations_list)
    print(observations_list)

