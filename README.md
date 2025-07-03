# InfluxDB Docker Classroom Setup

This repository provides a ready-to-use InfluxDB 2.x Docker setup for classroom and experimentation purposes. It includes instructions for running InfluxDB, loading sample time-series data, and exploring the data using Flux queries and the InfluxDB UI.


## Requirements

- **Docker Desktop** (Windows 11, macOS, or Linux)
- **Git** (to clone this repository)


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
- This will start InfluxDB 2.x on your machine, accessible at [http://localhost:8086](http://localhost:8086).

### 3. Log in to InfluxDB

- Open your browser and go to [http://localhost:8086](http://localhost:8086)
- **Username:** `admin`
- **Password:** `adminpassword`
- **Organization:** `example-org`
- **Bucket:** `example-bucket`

---

## Loading Sample Data

### Option 1: Use the UI to Load Air Sensor Sample Data

1. In the InfluxDB UI, go to **Data > Buckets** and confirm `example-bucket` exists.
2. Go to **Data > Tasks** and create a new task.
3. Paste the following Flux script (or use `sample_air_sensor.flux` if provided):
```
import "influxdata/influxdb/sample"

option task = {
name: "Collect air sensor sample data",
every: 15m,
}

sample.data(set: "airSensor")
|> to(bucket: "example-bucket")
```

4. Save and run the task. This will periodically load air sensor sample data into your bucket.


## Exploring Data

1. Go to the **Explore** tab in the InfluxDB UI.
2. Set the **time range** (top right) to a wide interval, such as **"All Time"** or the last 30 days.
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

---

## Troubleshooting

| Issue                        | Solution                                                                                               |
|------------------------------|--------------------------------------------------------------------------------------------------------|
| **No data in Explore tab**   | Set time range to "All Time". Use the Script Editor with the query above.                             |
| **Large response error**     | Use a narrower time range (e.g., `range(start: -7d)`) and/or increase the `aggregateWindow` interval. |
| **No graph, only columns**   | Ensure your query filters both measurement and fields as shown above.                                 |
| **Data not appearing**       | Refresh the UI or re-run the data loading task.                                                       |

## Credits

- [InfluxData Sample Data Documentation](https://docs.influxdata.com/influxdb/latest/sample-data/)
- [InfluxDB Docker Hub](https://hub.docker.com/_/influxdb)





