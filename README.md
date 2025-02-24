Business Introduction --
Velocity Railways is a leading railway operator based in the United Kingdom, dedicated to providing
efficient, reliable, and timely train services across the nation. The company leverages cutting-edge
technology and real-time data integration to ensure its
customers receive up-to-the-minute
information on train schedules, departures, and arrivals.
10Alytics
-- PROBLEM STATEMENT --
The company is currently facing challenges in providing accurate and real-time train departure information to its passengers.
The current system
provides scheduled
departure times but often lacks real-time updates on delays, cancellations, or other disruptions. The company wants to create a better pipeline that fetches real time data from a source and saves it on a database for further usages. Moreover, the company's existing data pipeline suffers from:
• Data quality issues due to incorrect or incomplete real-time updates.
• Inconsistent performance in stream processing and validation.
• Single-point failures with only one database for storage, causing outages when the system goes down.
• Lack of real-time monitoring and alerting, making it difficult to detect pipeline failures or performance bottlenecks.
8810Alytics
To address these issues, the company wants to build a robust, scalable data pipeline that does the following:
• processes both scheduled and real-time train departure data
• validates the data dynamically,
• stores it in two different databases for high availability.
The system should be fully orchestrated, monitored, and fault-tolerant.
8810 Alytics
The proposed solution should:

1. Provide accurate real-time train departure information by integrating a data source that
provides scheduled timetables, real-time train movements,


2. Ensure high data quality using a robust validation framework that dynamically adapts to
changes in data sources and formats.


3. Be fault-tolerant and highly available, ensuring the system can seamlessly failover to

backup systems (local PostgreSQL) if the primary system (Azure PostgreSQL) fails.

4. Enable real-time data processing to support dynamic dashboards, anomaly detection,
and decision-making.


5. Orchestrate complex data flows that support real-time data enrichment, processing,
validation, and storage in a reliable, scalable manner.Tech Stack
• Requests
• Apache Flink
• Great Expectations
• Airflow
• Azure
• PostgreSQL
• Python
88° 10Alytics
Highlevel Architecture
1. Ingestion Layer:
• Data pulled from train schedule APIs.
• Real-time data collected through Flink.
2. Data Validation:
• Great Expectations runs locally to validate ingested data.
• Validation results are logged and monitored before proceeding.
3. Data Duplication:
• Python scripts handle the duplication process, sending the data to both Azure PostgreSQL and local PostgreSQL for backup.
4. Orchestration:
• Airflow locally orchestrates the full pipeline, managing the ingestion, validation, and duplication of data.
Highlevel Architecture (cntd)
1. Monitoring & Failure Handling:
• If there's any issue with inserting data into Azure PostgreSQL, the data is safely backed up in local PostgreSQL, and notifications are triggered via Airflow. Data Source: Train Station Timetables API
The Train Station Timetables API provided by TransportAPI allows users to access realtime train departure information for specified train stations in the UK.
The endpoint GET /v3/uk/train/station_timetables/fid}.json returns a comprehensive timetable of train departures within a specified time window, including scheduled and realtime updates when the live=true parameter is set.
https://developer.transportapi.com/docs#get-/v3/uk/train/station_timetables/-id-.json
88 10Alytics
Key Features
• Timetable Information: Retrieves both scheduled departures and live updates for trains, offering a complete picture of train movements at a station.
• Custom Time Windows: Users can specify a time window by providing a datetime timestamp along with from_offset and to_offset parameters to tailor the results to their needs.
• Data Sources: The real-time information is sourced from open data systems such as the Network Rail TRUST system, Train Movements, and VSTP data feeds, ensuring accuracy and timeliness.
• Comprehensive Coverage: The API includes not only departures from the station of interest but also arrivals and passing trains, making it versatile for various applications such as mobile apps or web displays.
88 10Alytics
Highlevel Architecture
• Real-Time Data Ingestion: We will use Binance WebSocket API to fetch live market data for multiple cryptocurrency pairs
• Data Streaming with Google Pub/Sub: Google Pub/Sub will act as the messaging service to handle the streaming within the GCP environment
• Data Processing with Apache Beam: We will use Apache Beam - a real-time processing framework (via Cloud Dataflow) to transform, clean, and prepare the data.
• Storage in BigQuery: BigQuery will serve as the real-time data warehouse, allowing the company to query the latest price data and historical market information for analytics and reporting.
• Scalable and Cloud-Native: The entire architecture will seat on Google Cloud to ensure low maintenance overhead and adaptability for future requirements.Data Validation
Great Expectations ensures data quality by implementing dynamic, multi-level validation checks. Use Great Expectations to:
• Scheduled Timetables: Validate train departure times against known formats, ensuring the data makes sense (e.g., valid station codes and times).
• Real-Time Updates: Check if real-time data matches its expected schema and correlates with historical patterns (e.g., a sudden cancellation might trigger an alert).
• External Data (Weather/Social Media): Ensure that the weather
