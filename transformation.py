import pandas as pd
import time

import requests
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")

# List of station codes
station_ids = ["crs:RMD", "WAT", "LYM"]  # Replace with actual station codes

# Function to fetch timetable data for a list of stations
def fetch_station_timetables(app_id, api_key, station_ids):
    if not app_id or not api_key:
        print("API credentials are missing. Check your .env file.")
        return {}

    timetable_data = {}

    for station_id in station_ids:
        # Construct the API URL for the current station
        url = f"https://transportapi.com/v3/uk/train/station_timetables/{station_id}.json"
        
        # Define request parameters
        params = {
            "app_key": api_key,
            "app_id": app_id
        }
        
        # Make the API request
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            timetable_data[station_id] = data
            print(f"Successfully fetched data for station: {station_id}")
        else:
            print(f"Failed to fetch data for station: {station_id}. Status Code: {response.status_code}")
        
        # Respect API rate limits
        time.sleep(1)

    return timetable_data

# Fetch data for the stations
timetable_data = fetch_station_timetables(app_id, api_key, station_ids)


# Flatten and clean the timetable data
cleaned_data = []

for station_id, station_data in timetable_data.items():
    if 'departures' in station_data and 'all' in station_data['departures']:
        departures = station_data['departures']['all']
        for departure in departures:
            cleaned_entry = {
                'station_id': station_id,
                'train_uid': departure.get('train_uid'),
                'scheduled_departure_time': departure.get('aimed_departure_time'),
                'destination_name': departure.get('destination', [{}])[0].get('name'),
                'platform': departure.get('platform'),
                'operator_name': departure.get('operator_name'),
            }
            cleaned_data.append(cleaned_entry)

# Create a pandas DataFrame
df_timetable = pd.DataFrame(cleaned_data)

# Handle missing values
df_timetable.fillna("Unknown", inplace=True)

# Rename columns for clarity
df_timetable.rename(columns={
    'station_id': 'Station ID',
    'train_uid': 'Train UID',
    'scheduled_departure_time': 'Departure Time',
    'destination_name': 'Destination',
    'platform': 'Platform',
    'operator_name': 'Operator'
}, inplace=True)

# View the cleaned data
print("Cleaned Timetable Data:")
print(df_timetable)
