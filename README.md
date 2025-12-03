# InfluxDB Docker Classroom Setup

This repository provides a ready-to-use InfluxDB Docker setup for classroom and experimentation purposes. It includes instructions for running InfluxDB, loading sample time-series data, and exploring the data using Flux queries and the InfluxDB UI.


## Requirements

- **Docker Desktop** (Windows 11, macOS, or Linux)
- **Git** (to clone this repository)
- **VSCode** (to write or edit your code)
- **Python** (to execute you code)


## Getting Started

### 1. Clone the Repository
```
git clone https://github.com/yourusername/influxdb-docker-demo.git
cd influxdb-docker-demo
```

### 2. Start InfluxDB with Docker Compose
```
docker compose up -d
```
- This will start InfluxDB on your machine, accessible at [http://localhost:8086](http://localhost:8086).

### 3. Log in to InfluxDB

- Open your browser and go to [http://localhost:8086](http://localhost:8086)
- **Username:** `admin`
- **Password:** `adminpassword`

## Loading Sample Data

1. Create and activate a virtual environment (assuming that you are inside the project's folder):

```powershell
# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or on Windows Command Prompt
.\venv\Scripts\activate.bat

# Or on Linux/Mac
source venv/bin/activate
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Run the data loading script:
```
python load_sample_data.py
```

This will generate and load 48 hours of sample air sensor data (temperature, humidity, CO levels) from 4 different sensors.

## Exploring Data

1. Go to the **Data Explorer** tab in the InfluxDB UI.
2. Set the **time range** (top right) to a wide interval, or alternativelly 
3. Use the **Script Editor** and paste this query to see all air sensor data:
```
from(bucket: "example-bucket")
|> range(start: -7d)
|> filter(fn: (r) => r["_measurement"] == "airSensors")
|> filter(fn: (r) => r["_field"] == "co" or r["_field"] == "humidity" or r["_field"] == "temperature")
```
4. **Tip:** If you want smoother graphs, add aggregation:
```
|> aggregateWindow(every: 1h, fn: mean)
|> yield()
```

## Stopping the Stack

**To stop InfluxDB (keeps data):**
```
docker compose down
```

**To stop and remove all data (fresh start):**
```
docker compose down -v
```
This removes the containers and volumes, allowing you to start completely fresh on the next `docker compose up -d`.

**To manually clean up data directories:**
```powershell
# Windows PowerShell
Remove-Item -Recurse -Force .\data\*, .\config\*

# Linux/Mac
rm -rf ./data/* ./config/*
```

## Deactivating the Virtual Environment

When you are done working in your Python virtual environment, you can deactivate it by running:
```
deactivate
```
This works on Windows, Mac, and Linux.





