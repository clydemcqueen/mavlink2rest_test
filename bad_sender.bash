#!/usr/bin/env bash

while true
do

  curl --verbose http://127.0.0.1:6040/mavlink -H "accept: application/json" --data \
  '{
      "header": {
          "system_id": 1,
          "component_id": 194,
          "sequence": 52
      },
      "message": {
          "type": "DISTANCE_SENSOR",
          "time_boot_ms": 201509,
          "min_distance": 20,
          "max_distance": 5000,
          "current_distance": 2325,
          "mavtype": {"type": "MAV_DISTANCE_SENSOR_ULTRASOUND"},
          "id": 1,
          "orientation": {"type": "MAV_SENSOR_ROTATION_PITCH_270"},
          "covariance": 255,
          "horizontal_fov": 0.52,
          "vertical_fov": 0.52,
          "quaternion": [0, 0, 0, 0],
          "signal_quality": 0
      }
  }'

  sleep 0.5

done
