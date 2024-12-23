import pandas as pd
from sqlalchemy import create_engine

# Example timetable_data
timetable_data = {
    "station_1": {
        "departures": {
            "all": [
                {"train_uid": "A123", "aimed_departure_time": "08:30", "destination": [{"name": "City A"}], "platform": "1", "operator_name": "Operator A"},
                {"train_uid": "B456", "aimed_departure_time": "09:15", "destination": [{"name": "City B"}], "platform": "2", "operator_name": "Operator B"}
            ]
        }
    },
    "station_2": {
        "departures": {
            "all": [
                {"train_uid": "C789", "aimed_departure_time": "10:00", "destination": [{"name": "City C"}], "platform": "3", "operator_name": "Operator C"}
            ]
        }
    }
}

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

# Create DataFrame
df_timetable = pd.DataFrame(cleaned_data)

# Handle missing values
df_timetable.fillna("Unknown", inplace=True)

# Rename columns
df_timetable.rename(columns={
    'station_id': 'Station ID',
    'train_uid': 'Train UID',
    'scheduled_departure_time': 'Departure Time',
    'destination_name': 'Destination',
    'platform': 'Platform',
    'operator_name': 'Operator'
}, inplace=True)

# PostgreSQL credentials
host = 'localhost'
database = 'postgres'
user = 'postgres'
password = 'postgres'

# Create engine
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

# Write DataFrame to PostgreSQL
table_name = 'timetable'
df_timetable.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data successfully written to the '{table_name}' table.")
