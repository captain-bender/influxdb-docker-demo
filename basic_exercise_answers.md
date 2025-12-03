# Basic Exercise — Sample Answers

This file contains example Flux queries and short explanations for the three mini-projects from the exercise.

---

**1) Sensor Performance Over Time**

Goal: Plot the average temperature per hour for a specific sensor (example `TLM0100`) over the last 2 days and identify unusual spikes or drops.

Flux query:

```
from(bucket: "example-bucket")
|> range(start: -2d)
|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> yield(name: "mean_temperature_hourly")
```

Notes:
- Use the Data Explorer -> Query Builder and set the global UI time range to `Last 2 days` (or rely on the `range()` above).
- Look for hour buckets with values significantly different from the overall mean; you can add at the end of the previous query the additional text `|> map(fn: (r) => ({ r with deviation: r._value - mean }))` if you compute a baseline separately.

---

**2) Comparative Analysis (CO levels between two locations)**

Goal: Compare CO levels between two locations (e.g., `Warehouse-1` and `Office-1`) over the last 24 hours using hourly means.

Flux query:

```
from(bucket: "example-bucket")
|> range(start: -24h)
|> filter(fn: (r) => r._measurement == "airSensors" and r._field == "co" and (r.location == "Warehouse-1" or r.location == "Office-1"))
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> group(columns: ["location"])
|> yield(name: "co_by_location_hourly")
```

Notes:
- In the UI, the `location` tag will appear as separate series — you can compare them visually or export CSV and compute averages in Python/pandas.
- To compute which location had the higher average CO over the period, wrap this with a `mean()` per `location` or compute in Python after export.

Example to compute average CO per location (Flux):

```
from(bucket: "example-bucket")
|> range(start: -24h)
|> filter(fn: (r) => r._measurement == "airSensors" and r._field == "co")
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> group(columns: ["location"])
|> mean(column: "_value")
|> yield(name: "avg_co_per_location")
```

---

**3) Humidity Pattern Detection**

Goal: Find the maximum and minimum humidity values recorded by all sensors in the last 7 days and report which sensor(s) and timestamps recorded them.

Flux query (min and max):

```
maxHumidity = from(bucket: "example-bucket")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "humidity")
  |> top(n: 1, columns: ["_value"])

minHumidity = from(bucket: "example-bucket")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "airSensors" and r._field == "humidity")
  |> bottom(n: 1, columns: ["_value"])

union(tables: [maxHumidity, minHumidity])
|> yield(name: "min_and_max_humidity")
```

Notes:
- The returned records include `_time`, `_value` (the humidity), and tags like `sensor_id` and `location` so you can identify which sensor recorded the extrema.
- If you expect multiple sensors to share the same max/min value, increase `n` in `top()`/`bottom()` (for example `n: 5`).
 

<br>
<br>
<br>
<br>



## Line-by-line explanation

Below is a short, plain-English explanation of each line in the first query (the hourly average temperature for sensor `TLM0100`):

```
from(bucket: "example-bucket")
```
- "Look in the bucket named `example-bucket` for data." (choose the data source)

```
|> range(start: -2d)
```
- "Only consider data from the last two days (48 hours)." (time filter)

```
|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
```
- "Keep only records that are: part of the `airSensors` measurement, belong to sensor `TLM0100`, and are the `temperature` field." (narrow by measurement, tag, and field)

```
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
```
- "Group the data into one-hour buckets and compute the average (`mean`) temperature for each hour. Do not create empty buckets if there is no data for an hour." (aggregation)

```
|> yield(name: "mean_temperature_hourly")
```
- "Return the results and label the output `mean_temperature_hourly` so the output stream/table is named." (output)

Small extra note: the results will include columns like `_time` (hour timestamp), `_value` (the averaged temperature), and tags such as `sensor_id` and `location` to identify the source of each value.

