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

# Print the fetched data
print("Collected Timetable Data:")
print(timetable_data)