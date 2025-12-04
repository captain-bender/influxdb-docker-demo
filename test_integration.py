import pandas as pd
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient

# Fill in with your InfluxDB details
url = "http://localhost:8086"
token = "U7-lakyfaMe4rO6PlLO-3r8q8H12B_QBD9KbvGRr_ICokbnb-QwRgys4FkbQo2s6Vuu7AuSCzSJXx2mnOotiuA=="
org = "example-org"
bucket = "example-bucket"

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Example: Average temperature per hour for sensor TLM0100 over last 2 days
flux_query = '''
from(bucket: "example-bucket")
|> range(start: -2d)
|> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
|> aggregateWindow(every: 1h, fn: mean)
|> yield()
'''

tables = query_api.query(flux_query, org=org)

# Convert results to DataFrame
records = []
for table in tables:
    for record in table.records:
        records.append({
            "time": record.get_time(),
            "value": record.get_value()
        })

df = pd.DataFrame(records)
print(df.head())

# Plot the data
plt.plot(df["time"], df["value"])
plt.title("Average Temperature per Hour (TLM0100)")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()