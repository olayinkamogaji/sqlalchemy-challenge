import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Precipation: /api/v1.0/precipation, "
        f"Stations: /api/v1.0/stations, "
        f"Temperature: /api/v1.0/tobs, "
        f"Min Max Avg Temperature Start Date: /api/v1.0/<start>, "
        f"Min Max Avg Temperature Start Date, End Date: /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipation")
def precipation():
   
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()
    session.close()

    all_dates = {}
    prcp_list = []
    date_count = "2016-08-24"
    for date,prcp in results:
        if date == date_count:
            prcp_list.append(prcp)
        else:
            all_dates[date_count]=prcp_list
            prcp_list = [prcp]
            date_count = date       
    return jsonify(all_dates)
@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()
    session.close()

    all_dates = {}
    tobs_list = []
    date_count = "2016-08-24"
    for date,tobs in results:
        if date == date_count:
            tobs_list.append(tobs)
        else:
            all_dates[date_count]=tobs_list
            tobs_list = [tobs]
            date_count = date       
    return jsonify(all_dates)
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    all_temp = list(np.ravel(results))

    return jsonify(all_temp)
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_temp = list(np.ravel(results))

    return jsonify(all_temp)


if __name__ == '__main__':
    app.run(debug=True)
