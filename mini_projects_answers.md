# Mini Projects — Sample Answers

This file contains example Flux queries and short explanations for the three mini-projects from the exercise.

---

### Query 1 - Sensor Performance Over Time

Goal: Plot the average temperature per hour for a specific sensor (example `TLM0100`) over the last 2 days and identify unusual spikes or drops.

Flux query:

```
from(bucket: "example-bucket")
|> range(start: -2d)
|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> yield(name: "mean_temperature_hourly")
```

- `from(bucket: "example-bucket")`: "Look in the bucket named `example-bucket` for data." (choose the data source)

- `|> range(start: -2d)`: "Only consider data from the last two days (48 hours)." (time filter)


- `|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")`: "Keep only records that are: part of the `airSensors` measurement, belong to sensor `TLM0100`, and are the `temperature` field." (narrow by measurement, tag, and field)


- `|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)`:
"Group the data into one-hour buckets and compute the average (`mean`) temperature for each hour. Do not create empty buckets if there is no data for an hour." (aggregation)


- `|> yield(name: "mean_temperature_hourly")`: "Return the results and label the output `mean_temperature_hourly` so the output stream/table is named." (output)

---

### Query 2 — Line-by-line explanation (simple)

Query used:

```
from(bucket: "example-bucket")
|> range(start: -24h)
|> filter(fn: (r) => r._measurement == "airSensors" and r._field == "co" and (r.location == "Warehouse-1" or r.location == "Office-1"))
|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
|> group(columns: ["location"])
|> yield(name: "co_by_location_hourly")
```

- `from(bucket: "example-bucket")`: choose the `example-bucket` as the data source.
- `|> range(start: -24h)`: only look at the last 24 hours of data.
- `|> filter(...)`: keep only records from the `airSensors` measurement where the field is `co` and the `location` tag is either `Warehouse-1` or `Office-1` (so we compare those two locations).
- `|> aggregateWindow(every: 1h, fn: mean, createEmpty: false)`: group values into one-hour buckets and compute the mean CO for each hour; skip empty buckets.
- `|> group(columns: ["location"])`: group the results by the `location` tag so each location becomes its own series/table.
- `|> yield(name: "co_by_location_hourly")`: output the results labeled `co_by_location_hourly`.

Small extra note: the returned tables will include `_time` (bucket timestamp), `_value` (hourly average CO), and the `location` tag so you can visually compare the two locations or export to CSV.

### Query 3 — Line-by-line explanation (simple)

Query used (min and max humidity):

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

- `maxHumidity = from(bucket: "example-bucket")`: start a pipeline named `maxHumidity` pulling from `example-bucket`.
- `|> range(start: -7d)`: limit to the last 7 days.
- `|> filter(...)`: keep only the `humidity` field from the `airSensors` measurement.
- `|> top(n: 1, columns: ["_value"])`: pick the single record with the highest `_value` (the maximum humidity). Increase `n` if you want ties.

- `minHumidity = from(bucket: "example-bucket")`: start a second pipeline for the minimum value.
- `|> range(start: -7d)`: same 7‑day window as above.
- `|> filter(...)`: same humidity filter.
- `|> bottom(n: 1, columns: ["_value"])`: pick the single record with the lowest `_value` (the minimum humidity).

- `union(tables: [maxHumidity, minHumidity])`: combine the max and min pipelines into a single output stream.
- `|> yield(name: "min_and_max_humidity")`: return the combined results labeled `min_and_max_humidity`.

