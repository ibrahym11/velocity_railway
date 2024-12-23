from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import time
import os
from dotenv import load_dotenv

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define station IDs (modify this list as needed)
station_ids = ["crs:RMD", "WAT", "LYM"]

# Load environment variables from .env
def load_env_variables():
    load_dotenv()

# Function to fetch timetables
def fetch_station_timetables(**kwargs):
    # Load credentials from environment variables
    app_id = os.getenv("APP_ID")
    api_key = os.getenv("API_KEY")

    if not app_id or not api_key:
        raise ValueError("API credentials are missing. Check your .env file.")

    station_ids = kwargs.get("station_ids", [])
    timetable_data = {}

    for station_id in station_ids:
        url = f"https://transportapi.com/v3/uk/train/station_timetables/{station_id}.json"
        params = {
            "app_key": api_key,
            "app_id": app_id
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            timetable_data[station_id] = data
            print(f"Successfully fetched data for station: {station_id}")
        else:
            print(f"Failed to fetch data for station: {station_id}. Status Code: {response.status_code}")
        time.sleep(1)  # Rate-limiting

    # Push the data to XCom for later use
    return timetable_data

# Function to process and save the data
def process_and_save_timetable_data(**kwargs):
    ti = kwargs['ti']
    timetable_data = ti.xcom_pull(task_ids='fetch_timetables')

    if timetable_data:
        print("Collected Timetable Data:")
        print(timetable_data)
        # Here you can save to a database, file, or another system

# Define the DAG
with DAG(
    dag_id="fetch_train_timetables",
    default_args=default_args,
    description="Fetch train station timetables using Airflow",
    schedule_interval=None,  # Trigger manually for testing
    start_date=datetime(2024, 12, 10),
    catchup=False,
) as dag:

    # Task to load environment variables
    load_env_task = PythonOperator(
        task_id="load_env",
        python_callable=load_env_variables,
    )

    # Task to fetch station timetables
    fetch_timetables_task = PythonOperator(
        task_id="fetch_timetables",
        python_callable=fetch_station_timetables,
        op_kwargs={"station_ids": station_ids},
    )

    # Task to process and save the data
    process_save_task = PythonOperator(
        task_id="process_save_data",
        python_callable=process_and_save_timetable_data,
    )

    # Define task dependencies
    load_env_task >> fetch_timetables_task >> process_save_task
