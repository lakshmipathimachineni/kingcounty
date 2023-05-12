from typing import List
from flask import Flask, request, jsonify
import pandas as pd

import sqlite3
from initialize import initilize
from initialize import StopOut


initilize()
app = Flask(__name__)


# Define the API endpoints
@app.route('/')
def home():
    return 'Welcome to the King County Bus Transport !!'

@app.route('/get_all_trip_details/<trip_ids>', methods=['GET'])
def read_stops(trip_ids):
    conn = sqlite3.connect('bus_transport.db')
    cursor = conn.cursor()
    cursor.execute(" select a.trip_id, b.stop_id,b.stop_code,b.stop_name,b.stop_desc,b.stop_lat,b.stop_lon, b.zone_id,b.stop_url,b.location_type,b.parent_station,b.stop_timezone\
     from stop_times a , stops b where a.trip_id in ('"+trip_ids+"') and a.stop_id =  b.stop_id")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([StopOut(
        trip_id = row[0], stop_id=row[1],stop_code = row[2],stop_name= row[3],stop_desc= row[4],stop_lat= row[5],stop_lon= row[6]).__dict__ for row in rows])
