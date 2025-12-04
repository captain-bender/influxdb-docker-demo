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

### 4. Exploring Data

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

## Experiment with exercises
- Beasic Flux examples [here](./flux_basic_examples.md)
- Mini projects [here](./mini_projects.md)
- Integration exercises with Python [here](./integration_exercise.md)

## Stopping the Stack

**To stop and remove all data (fresh start):**
If you want to stop the stack and remove all containers, images and data so the next `up` starts from a fresh state, follow the commands below.

- Using Docker Compose: this stops services, removes containers, networks, images that were built by Compose, and deletes named volumes created by the compose file. WARNING: deleting volumes will permanently remove the database contents.

In order to stop the execution, please press CTRL+C, and then

```powershell
cd C:\Users\<your path>\Documents\mysql-docker-demo
docker compose down --rmi all -v --remove-orphans
```

- What the flags do:
	- `--rmi all`: removes images built by Compose (your `classicmodels-mysql` image created by `build`).
	- `-v`: removes named volumes declared in `docker-compose.yml` (this deletes DB data).
	- `--remove-orphans`: removes containers from previous runs that are not defined in this compose file.


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





