# Flux — Very Basic Examples

This file contains 5 very simple Flux queries and a plain-language, line-by-line explanation for each. Use these as copy/paste starters in the InfluxDB UI.

---

## Example 1 — Hourly average temperature for one sensor (last 2 days)

Query:
```
from(bucket: "example-bucket")
|> range(start: -2d)
|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> yield(name: "mean_temperature_hourly")
```
Explanation (line-by-line):
- `from(bucket: "example-bucket")`: Select the bucket `example-bucket` as the data source.
- `|> range(start: -2d)`: Only include data from the last 2 days.
- `|> filter(...)`: Keep only records where the measurement is `airSensors`, the tag `sensor_id` equals `TLM0100`, and the field is `temperature`.
- `|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)`: Group data into 1-hour buckets and compute the average temperature per bucket. Skip empty buckets.
- `|> yield(name: "mean_temperature_hourly")`: Output the resulting series labeled `mean_temperature_hourly`.

---

## Example 2 — Latest temperature reading per sensor (last hour)

Query:
```
from(bucket: "example-bucket")
|> range(start: -1h)
|> filter(fn: (r) => r._measurement == "airSensors" and r._field == "temperature")
|> group(columns: ["sensor_id"]) 
|> last()
|> yield(name: "latest_temperature_per_sensor")
```
Explanation:
- `from(bucket: "example-bucket")`: Use `example-bucket`.
- `|> range(start: -1h)`: Look at the last 1 hour of data.
- `|> filter(...)`: Keep only `temperature` field records from the `airSensors` measurement.
- `|> group(columns: ["sensor_id"])`: Group the data by `sensor_id` tag so operations apply per sensor.
- `|> last()`: Return the most recent record in each group (the latest reading per sensor).
- `|> yield(...)`: Output labeled results.

Notes: Useful to see the current reading for each sensor.

---

## Example 3 — Count readings per sensor (last 24 hours)

Query:
```
from(bucket: "example-bucket")
|> range(start: -24h)
|> filter(fn: (r) => r._measurement == "airSensors")
|> group(columns: ["sensor_id"]) 
|> count(column: "_value")
|> yield(name: "count_per_sensor")
```
Explanation:
- `from(bucket: "example-bucket")`: Select the bucket.
- `|> range(start: -24h)`: Use the last 24 hours.
- `|> filter(...)`: Keep all measurements from `airSensors` (all fields).
- `|> group(columns: ["sensor_id"])`: Group rows by `sensor_id` tag.
- `|> count(column: "_value")`: Count how many data points each group has (counts `_value` occurrences).
- `|> yield(...)`: Output counts per sensor.

Notes: Use this to check sensor activity (missing sensors will show zero rows).

---

## Example 4 — Max and min humidity over the last 7 days

Query:
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
Explanation:
- `maxHumidity = from(...)`: Start a pipeline named `maxHumidity` pulling from the bucket.
- `|> range(start: -7d)`: Limit to the last 7 days.
- `|> filter(...)`: Keep only `humidity` field records from `airSensors`.
- `|> top(n: 1, columns: ["_value"])`: Select the single record with the highest humidity value.
- `minHumidity = from(...) ... |> bottom(n: 1, columns: ["_value"])`: Same as above but choose the lowest humidity.
- `union(tables: [maxHumidity, minHumidity])`: Combine the two results into one output.
- `|> yield(...)`: Output labeled results.

Notes: Returned records include `_time` (when), `_value` (humidity), and tags like `sensor_id` and `location`.

---

## Example 5 — Smoothed hourly CO (3-hour moving average)

Query:
```
from(bucket: "example-bucket")
|> range(start: -48h)
|> filter(fn: (r) => r._measurement == "airSensors" and r._field == "co")
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> movingAverage(n: 3)
|> yield(name: "co_hourly_moving_avg")
```
Explanation:
- `from(bucket: "example-bucket")`: Choose the data bucket.
- `|> range(start: -48h)`: Use the last 48 hours of data.
- `|> filter(...)`: Keep only `co` field readings from `airSensors`.
- `|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)`: Aggregate into hourly means.
- `|> movingAverage(n: 3)`: Smooth the hourly mean series by computing a 3-point moving average (each point is the mean of current and previous 2 hour values).
- `|> yield(...)`: Output the smoothed series.

Notes: Moving average helps reduce short-term noise and show trends.

---

## How to use these
- Paste any query into the InfluxDB UI Explore -> Script Editor and run it. Adjust `range()` and tag values (`sensor_id`, `location`) to match your dataset.
