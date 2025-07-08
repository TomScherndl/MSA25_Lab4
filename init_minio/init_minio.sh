#!/usr/bin/env sh

while ! mc alias set local http://minio:9000 admin password > /dev/null 2>&1; do
  sleep 2
done

mc mb --ignore-existing local/weather-data
mc mb --ignore-existing local/retail-data

for file in /init_minio/gold/*; do
  filename=$(basename "$file")
  
  if [ "$filename" = "weather_aggregated.parquet" ]; then
    echo "→ Uploading to weather-data"
    mc cp "$file" local/weather-data/gold/
  else
    echo "→ Uploading to retail-data"
    mc cp "$file" local/retail-data/gold/
  fi
done