#!/usr/bin/env bash

while true
do

  curl --verbose http://127.0.0.1:6040/mavlink -H "accept: application/json" --data \
  '{
      "header": {
          "system_id": 255,
          "component_id": 240,
          "sequence": 52
      },
      "message": {
          "type": "COMMAND_LONG",
          "param1": 1.0,
          "param2": 0.0,
          "param3": 0.0,
          "param4": 0.0,
          "param5": 0.0,
          "param6": 0.0,
          "param7": 0.0,
          "command": {"type": "MAV_CMD_COMPONENT_ARM_DISARM"},
          "target_system": 1,
          "target_component": 1,
          "confirmation": 1
      }
  }'

  sleep 0.1

done
