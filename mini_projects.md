# Mini Projects: Analyzing Environmental Air Sensor Data with InfluxDB

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
Choose one of the following mini-projects (or propose your own):

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

Sample answers [here](./mini_projects_answers.md) 