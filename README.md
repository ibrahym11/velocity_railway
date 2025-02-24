# Velocity Railways Real-Time Train Departure Data Pipeline

## Introduction
Velocity Railways is a leading railway operator in the United Kingdom, committed to delivering efficient, reliable, and timely train services. To enhance customer experience, we are developing a **real-time train departure data pipeline** that ensures passengers receive accurate and up-to-the-minute information on train schedules, departures, and arrivals.

## Problem Statement
The current system provides scheduled departure times but lacks real-time updates on delays, cancellations, and disruptions. Additionally, the existing data pipeline suffers from:
- **Data quality issues** due to incorrect or incomplete real-time updates.
- **Inconsistent performance** in stream processing and validation.
- **Single-point failures**, with only one database for storage, leading to outages.
- **Lack of real-time monitoring and alerting**, making it difficult to detect pipeline failures or bottlenecks.

## Solution Overview
The proposed solution aims to build a **robust, scalable, and fault-tolerant data pipeline** that:
- Processes both scheduled and real-time train departure data.
- Dynamically validates data quality.
- Stores data in **two separate databases** (Azure PostgreSQL & Local PostgreSQL) for high availability.
- Ensures full orchestration, monitoring, and fault tolerance.

## Key Features
1. **Accurate real-time train departure information** by integrating scheduled timetables and real-time train movements.
2. **Dynamic data validation** using a robust framework adaptable to changing data sources and formats.
3. **High availability and fault tolerance** with automatic failover to a backup database.
4. **Real-time data processing** to support dynamic dashboards, anomaly detection, and decision-making.
5. **Efficient orchestration** of data ingestion, validation, and storage with real-time monitoring.

## Tech Stack
- **Requests** (for API calls)
- **Apache Flink** (for real-time data processing)
- **Great Expectations** (for data validation)
- **Airflow** (for orchestration)
- **Azure PostgreSQL & Local PostgreSQL** (for storage)
- **Python** (for scripting and pipeline management)

## High-Level Architecture
### 1. Ingestion Layer
- Data is pulled from the **Train Station Timetables API**.
- **Apache Flink** processes real-time data streams.

### 2. Data Validation
- **Great Expectations** ensures data integrity before storage.
- Validation results are logged and monitored.

### 3. Data Duplication & Storage
- **Python scripts** duplicate data and store it in both **Azure PostgreSQL** and **Local PostgreSQL**.

### 4. Orchestration
- **Apache Airflow** manages the data pipeline workflows.

### 5. Monitoring & Failure Handling
- If **Azure PostgreSQL** fails, data is backed up in **Local PostgreSQL**.
- **Airflow triggers alerts** in case of failures.

## Data Source: Train Station Timetables API
- API Endpoint: [`GET /v3/uk/train/station_timetables/{id}.json`](https://developer.transportapi.com/docs#get-/v3/uk/train/station_timetables/-id-.json)
- Provides real-time train departure information using:
  - **Scheduled Timetables**
  - **Live Updates**
  - **Custom Time Windows**
  - **Comprehensive Coverage** (departures, arrivals, and passing trains)

## Data Validation with Great Expectations
- **Scheduled Timetables**: Ensures correct formats (e.g., valid station codes and times).
- **Real-Time Updates**: Checks schema consistency and historical correlation.
- **External Data (Weather/Social Media)**: Enhances data reliability.

## Deployment
### **Prerequisites**
1. **Python 3.8+** installed.
2. **Apache Flink, Airflow, PostgreSQL** set up.
3. **TransportAPI key** for accessing real-time train data.

### **Setup Instructions**
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/velocity-railways-pipeline.git
   cd velocity-railways-pipeline
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure Airflow:**
   ```sh
   airflow db init
   airflow webserver &
   airflow scheduler &
   ```
4. **Run the pipeline:**
   ```sh
   python run_pipeline.py
   ```

## Future Enhancements
- Integration with additional **data sources** (e.g., weather data for delay predictions).
- Advanced **real-time analytics** and anomaly detection.
- Migration to **fully managed cloud solutions** for scalability.

## Contributors
- **Velocity Railways Data Engineering Team**
- **10Alytics Consulting**

## License
This project is licensed under the MIT License.

