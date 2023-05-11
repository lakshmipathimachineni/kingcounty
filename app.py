from typing import List
from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

# Read CSV files into data frames
stops_df = pd.read_csv('stops.csv')
routes_df = pd.read_csv('routes.csv')
stop_times_df = pd.read_csv('aggregated_stop_times.csv')

# Create the database engine
engine = create_engine('sqlite:///bus_transport.db', echo=True)

# Declare the database schema
Base = declarative_base()

class Stop(Base):
    __tablename__ = 'stops'
    stop_id = Column(Integer, primary_key=True)
    stop_name = Column(String)
    stop_lat = Column(Float)
    stop_lon = Column(Float)

class Route(Base):
    __tablename__ = 'routes'
    route_id = Column(Integer, primary_key=True)
    route_short_name = Column(String)
    route_desc = Column(String)

class StopTime(Base):
    __tablename__ = 'stop_times'
    trip_id = Column(Integer, primary_key=True)
    stop_ids = Column(String)

# Create the tables in the database
Base.metadata.create_all(engine)

# Insert data into the tables
stops_df.to_sql('stops', con=engine, if_exists='append', index=False)
routes_df.to_sql('routes', con=engine, if_exists='append', index=False)
stop_times_df.to_sql('stop_times', con=engine, if_exists='append', index=False)

# Create the Flask app
app = Flask(__name__)



# Define the request/response models
class StopIn:
    def __init__(self, stop_name: str, stop_lat: float, stop_lon: float):
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

class StopOut:
    def __init__(self, stop_id: int, stop_name: str, stop_lat: float, stop_lon: float):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

# Define the API endpoints
@app.route('/')
def home():
    return 'Welcome to the King County Bus Transport !!'

@app.route('/stops/', methods=['GET', 'POST'])

@app.route('/stops/', methods=['POST'])
def create_stop():
    stop = StopIn(**request.json)
    conn = sqlite3.connect('bus_transport.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stops (stop_name, stop_lat, stop_lon) VALUES (?, ?, ?)',
                   (stop.stop_name, stop.stop_lat, stop.stop_lon))
    conn.commit()
    stop_id = cursor.lastrowid
    cursor.execute('SELECT * FROM stops WHERE stop_id = ?', (stop_id,))
    row = cursor.fetchone()
    conn.close()
    return jsonify(StopOut(stop_id=row[0], stop_name=row[1], stop_lat=row[2], stop_lon=row[3]).__dict__)

@app.route('/stops/', methods=['GET'])
def read_stops():
    conn = sqlite3.connect('bus_transport.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stops')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([StopOut(stop_id=row[0], stop_name=row[1], stop_lat=row[2], stop_lon=row[3]).__dict__ for row in rows])
