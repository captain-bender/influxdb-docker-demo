# Exercise: Analyzing Environmental Air Sensor Data with InfluxDB

## Objective
Explore, analyze, and visualize environmental air sensor data stored in InfluxDB. Use Flux queries to extract insights and Python (pandas/matplotlib) to create at least one visualization for your findings.

## Instructions
1. Connect to InfluxDB
    - Access the InfluxDB UI at http://localhost:8086.

    - Use the credentials provided by your instructor.

2. Explore the Air Sensor Dataset
    - In the Explore tab, select the example-bucket and the airSensors measurement.

    - Familiarize yourself with the available fields: co, humidity, temperature, and tags such as sensor_id or location.

3. Write and Run Flux Queries
Choose one of the following mini-projects (or propose your own, with approval):

    A. Sensor Performance Over Time

    - Plot the average temperature per hour for a specific sensor (e.g., sensor_id = TLM0100) over the last 2 days.

    - Identify any periods where temperature readings spike or drop unusually.

    B. Comparative Analysis

    - Compare CO levels between two different locations over the last 24 hours.

    - Which location had higher average CO concentration? Are there any notable trends?

    C. Humidity Pattern Detection

    - Find the maximum and minimum humidity values recorded by all sensors in the last 7 days.

    - Identify which sensor(s) recorded these values and at what times.

    Example Flux Query for A:
    ```
    from(bucket: "example-bucket")
    |> range(start: -2d)
    |> filter(fn: (r) => r._measurement == "airSensors" and r.sensor_id == "TLM0100" and r._field == "temperature")
    |> aggregateWindow(every: 1h, fn: mean)
    |> yield()
    ```
4. Export Data for Visualization
- Use the InfluxDB UI to export query results as CSV (look for the download/export button).

- Alternatively, use Python to query InfluxDB directly (optional advanced step).

5. Visualize with Python (pandas/matplotlib)
- Load the CSV into pandas and create a relevant plot (e.g., line chart for temperature trends, bar chart for CO comparison).

    Example code:
    ```python
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv("your_exported_data.csv")
    df['time'] = pd.to_datetime(df['_time'])
    plt.plot(df['time'], df['_value'])
    plt.title("Average Temperature per Hour (TLM0100)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig("temperature_trend.png")
    plt.show()
    ```
6. Prepare Your Slides
- Slide 1: Briefly describe your analysis question and approach.

- Slide 2: Show your Flux query, a summary of results, and your visualization.

- Slide 3 (optional): Discuss any interesting findings, anomalies, or potential real-world implications.

## Optional: Connect to InfluxDB Using Python and Query Data Directly
Instead of exporting CSVs from the InfluxDB UI, you can use Python to connect to your InfluxDB instance, run Flux queries, and visualize the results with pandas and matplotlib.

1. Install the InfluxDB Python Client. In your terminal or command prompt, run:
```
pip install influxdb-client pandas matplotlib
```

2. Gather Your Connection Details
You’ll need:

- URL: Usually http://localhost:8086

- Token: (Find this in InfluxDB UI under Data > Tokens. Use your All-Access or generated token.)

- Org: (Your organization name, e.g., example-org)

- Bucket: (e.g., example-bucket)

3. Example Python Script to Query and Visualize Data
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

4. Experiment and Extend
- Try changing the Flux query to analyze different sensors, fields (co, humidity), or time windows.

- Use DataFrame methods to further analyze or aggregate the data before plotting.