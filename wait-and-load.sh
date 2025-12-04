#!/bin/sh
set -eu

# Default values
INFLUX_URL="${INFLUX_URL:-http://influxdb:8086}"
MAX_RETRIES="${MAX_RETRIES:-60}"
SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

INFLUX_HEALTH_URL="${INFLUX_URL%/}/health"

echo "Waiting for InfluxDB at ${INFLUX_HEALTH_URL}..."

i=0
while [ "$i" -lt "$MAX_RETRIES" ]; do
  i=$((i+1))
  if curl -fsS "$INFLUX_HEALTH_URL" 2>/dev/null | grep -q '"status":"pass"'; then
    echo "InfluxDB healthy"
    break
  fi
  echo "Not ready yet (attempt $i/$MAX_RETRIES). Sleeping $SLEEP_SECONDS s..."
  sleep "$SLEEP_SECONDS"
done

if [ "$i" -ge "$MAX_RETRIES" ]; then
  echo "Timed out waiting for InfluxDB after $MAX_RETRIES attempts" >&2
  exit 1
fi

echo "Running loader script..."
python load_sample_data.py

echo "Loader finished."
