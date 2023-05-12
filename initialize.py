import os
from typing import List
from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import requests
import zipfile

url = "https://metro.kingcounty.gov/GTFS/google_transit.zip"
save_path = "download.zip"

def extractZip(save_path):
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        # Extract all files and folders in the current directory
        zip_ref.extractall()
        
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied: Unable to delete file '{file_path}'.")
        
        
def delete_all_txtfile():
    folder_path = os.getcwd()

# Get a list of all files in the current folder
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        if file_name.endswith(".txt"):
            # Construct the file path
            file_path = os.path.join(folder_path, file_name)
            
            # Delete the file
            os.remove(file_path)
        
delete_file("bus_transport.db")
delete_all_txtfile()

# Create the tables in the database

# Define the request/response models
class StopIn:
    def __init__(self, stop_name: str, stop_lat: float, stop_lon: float):
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

class StopOut:
    def __init__(self,trip_id:int, stop_id:int,stop_code:String,stop_name:String,stop_desc:String,stop_lat:float,stop_lon:float):
       self.trip_id = trip_id 
       self.stop_id = stop_id 
       self.stop_code = stop_code
       self.stop_name =  stop_name
       self.stop_desc =  stop_desc
       self.stop_lat =  stop_lat
       self.stop_lon =  stop_lon 
      
      
      
        
def download_csv(url, save_path):
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV file downloaded successfully and saved at: {save_path}")
    else:
        print("Failed to download CSV file.")

def renameTxttoCSV():
    file_list = os.listdir()

    # Iterate over each file in the directory
    for file_name in file_list:
        if file_name.endswith(".txt"):
            # Rename the file by replacing the extension
            new_file_name = os.path.splitext(file_name)[0] + ".csv"

            if os.path.exists(new_file_name):
                os.remove(new_file_name)  # Delete the existing file

            os.rename(file_name, new_file_name)


def initilize():
    download_csv(url, save_path)
    extractZip(save_path)
    renameTxttoCSV()
    # Create the database engine
    engine = create_engine('sqlite:///bus_transport.db', echo=True)

    # Declare the database schema
    Base = declarative_base()
    Base.metadata.create_all(engine)
    stops_df = pd.read_csv('stops.csv')
    stops_times_df = pd.read_csv('stop_times.csv')
    routes_df = pd.read_csv('routes.csv')
    stops_df.to_sql('stops', con=engine, if_exists='replace', index=False)
    routes_df.to_sql('routes', con=engine, if_exists='replace', index=False)
    stops_times_df.to_sql('stop_times', con=engine, if_exists='replace', index=False)

    