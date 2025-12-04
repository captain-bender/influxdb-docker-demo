## Integration Exercise: Connect to InfluxDB Using Python and Query Data Directly
Instead of exporting CSVs from the InfluxDB UI, you can use Python to connect to your InfluxDB instance, run Flux queries, and visualize the results with pandas and matplotlib.

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

3. Gather Your Connection Details
You’ll need:

- URL: Usually http://localhost:8086

- Generate a new API Token: (Find this in InfluxDB UI under Load Data > API Tokens. Use "All Access API Token" option.)

- Org: (Your organization name, e.g., example-org)

- Bucket: (e.g., example-bucket)

4. Example Python Script to Query and Visualize Data
Replace the variables with your actual values:
    ```python
    import pandas as pd
    import matplotlib.pyplot as plt
    from influxdb_client import InfluxDBClient

    # Fill in with your InfluxDB details
    url = "http://localhost:8086"
    token = "YOUR_TOKEN_HERE"
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
    ```
    This script connects to your InfluxDB, runs a Flux query, loads the results into a pandas DataFrame, and plots the temperature trend.

5. Experiment and Extend
- Try changing the Flux query to analyze different sensors, fields (co, humidity), or time windows.

- Use DataFrame methods to further analyze or aggregate the data before plotting.

6. Complete your experiments and type **deactivate** to terminal ine order to stop venv.