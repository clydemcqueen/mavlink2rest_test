This is a test harness for tracking down https://github.com/bluerobotics/BlueOS-docker/issues/1740.
I'm trying to use BlueOS code and mavlink2rest to send MAVLink messages, and then look for CRC problems.
But I'm stuck just getting mavlink2rest to work from the command line.

Add these paths to the Python path:
* BlueOS-docker/core/services/ping
* BlueOS-docker/core/libs/commonwealth

Download the latest mavlink2rest binary from https://github.com/mavlink/mavlink2rest

Run mavlink2rest:
~~~
./mavlink2rest-x86_64-unknown-linux-musl --verbose --system-id 255 --component-id 0 --connect udpin:0.0.0.0:14550 --server 127.0.0.1:6040
~~~

[Handy swagger API](http://127.0.0.1:6040/docs/index.html?url=/docs.json#/default/get_helper_mavlink)

Test: use curl to send a COMMAND_LONG message:
~~~
curl --verbose http://127.0.0.1:6040/mavlink -H "accept: application/json" --data \
'{
    "header": {
        "system_id": 255,
        "component_id": 240,
        "sequence": 0
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
~~~

Send a DISTANCE_SENSOR message:
~~~
curl --verbose http://127.0.0.1:6040/mavlink -H "accept: application/json" --data \
'{
    "header": {
        "system_id": 255,
        "component_id": 240,
        "sequence": 0
    },
    "message": {
        "type": "DISTANCE_SENSOR",
        "time_boot_ms": 15142,
        "min_distance": 20,
        "max_distance": 5000,
        "current_distance": 33,
        "mavtype": {"type": "MAV_DISTANCE_SENSOR_ULTRASOUND"},
        "id": 1,
        "orientation": {"type": "MAV_SENSOR_ROTATION_PITCH_270"},
        "covariance": 255,
        "horizontal_fov": 0.52,
        "vertical_fov": 0.52,
        "quaternion": [1.0, 0.0, 0.0, 0.0],
        "signal_quality": 0
    }
}'
~~~

[main.py](main.py) produces this result:
~~~
2023-07-09 17:33:22.196 | INFO     | ping1d_mavlink:send_distance_data:63 - sending 333 (0)
...
~~~