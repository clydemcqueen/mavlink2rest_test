This is a test harness for tracking down https://github.com/bluerobotics/BlueOS-docker/issues/1740.

This example does not use a mavlink router (e.g., mavlink-routerd), so you can only have 1 receiver: QGC or recv.py.

Add these paths to the Python path:
* BlueOS-docker/core/services/ping
* BlueOS-docker/core/libs/commonwealth
* ardusub_log_tools

Download the latest mavlink2rest binary from https://github.com/mavlink/mavlink2rest

Run mavlink2rest:
~~~
./mavlink2rest-x86_64-unknown-linux-musl --verbose --system-id 255 --component-id 0 --connect udpout:127.0.0.1:14550 --server 127.0.0.1:6040
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
        "signal_quality": 100
    }
}'
~~~

[send.py](send.py) produces this result:
~~~
2023-07-09 17:33:22.196 | INFO     | ping1d_mavlink:send_distance_data:63 - sending 333 (0)
...
~~~

A tlog file with a bad message:
~~~
(install_pymavlink_local) clyde@fastr:~/Documents/QGroundControl/Telemetry$ tlog_bad_data.py --verbose "2023-07-09 18-47-55.tlog"
Processing 1 files
-------------------
Results for 2023-07-09 18-47-55.tlog
BadDataMsg mavlink2=True sysid=1 compid=194 msg_id=132 reason: invalid MAVLink CRC in msgID 132 0xf58d should be 0x7e2f
msg_id 132 count 1
1 BAD_DATA messages, 1 of them were CRC errors
~~~

Hand-parse a bad DISTANCE_SENSOR msg:
~~~
                        hex             dec
MAVLink 2 packet format https://mavlink.io/en/guide/serialization.html
magic                   FD
len                     16              22          Length of payload (quaterion and signal_quality are missing)
incompat_flags          00              0           No signature
compat_flags            00              0
seq                     34              52
sysid                   01              1
compid                  C2              194
msgid                   84 00 00        132
    DISTANCE_SENSOR payload https://mavlink.io/en/messages/common.html#DISTANCE_SENSOR
    time_boot_ms        25 13 03 00     201509
    min_distance        14 00           20
    max_distance        88 13           5000
    current_distance    15 09           2325
    type                01              1
    id                  01              1
    orientation         19              25
    covariance          FF              255
    horizontal_fov      B8 1E 05 3F     5.2e-01
    vertical_fov        B8 1E 05 3F     5.2e-01
    quaternion          missing, it is zero
    signal_quality      missing, must be zero ???
checksum                8D F5           62861
signature               not there -- optional
~~~

[QGC prefixes a 64-bit timestamp](https://github.com/mavlink/qgroundcontrol/blob/245f9f1f9c475a24b02271e0b1a7a150f601f80d/src/comm/MAVLinkProtocol.cc#L280)
in big-endian format just before the 0xFD:
~~~
Timestamp of this message:
00 06 00 18 28 DD 1E B8     1688953625059000     
Timestamp of next message:
00 06 00 18 28 DE CC 68     1688953625169000
~~~

Send this bad message via curl:
~~~
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
~~~

All of these will end up in a tlog file with bad CRC values.

Note that the sequence number is ignored by mavlink2rest; seq is assigned by the underlying Rust library.
Therefore, the CRC values are all different, making this annoying to test.

Next steps:
* set up a router (mavproxy?)
* look at CRC values in pymavlink (good, since they don't crash)
* look at CRC values in tlog files (bad, since they do crash)
* then look at QGC code, why is it bad?

Launch mavproxy.py (TODO TODO TODO)
~~~
SIM_VEHICLE: "mavproxy.py" "--out" "127.0.0.1:14550" "--master" "tcp:127.0.0.1:5760" "--sitl" "127.0.0.1:5501" "--out" "udp:0.0.0.0:14550" "--console"
RiTW: Starting ArduSub : /home/clyde/ardupilot/build/sitl/bin/ardusub -S --model vectored_6dof --speedup 1 --slave 0 --defaults Tools/autotest/default_params/sub-6dof.parm --sim-address=127.0.0.1 -I0 --home 33.810313,-118.39386700000001,0.0,270.0
Connect tcp:127.0.0.1:5760 source_system=255

~~~

I'm getting zeros at the end... is mavlink2rest sending 0s?
~~~
/home/clyde/venv/mavlink2rest_test/bin/python /home/clyde/projects/mavlink2rest_test/recv.py 
msgbuf ::: fd 27 00 00 b8 01 c2 84 00 00 25 13 03 00 14 00 88 13 15 09 01 01 19 ff b8 1e 05 3f b8 1e 05 3f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 56 1c ::: seq 184 sysid 1 compid 194 msgid DISTANCE_SENSOR crc 7254
msgbuf ::: fd 27 00 00 ba 01 c2 84 00 00 25 13 03 00 14 00 88 13 15 09 01 01 19 ff b8 1e 05 3f b8 1e 05 3f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 8b 0a ::: seq 186 sysid 1 compid 194 msgid DISTANCE_SENSOR crc 2699
msgbuf ::: fd 27 00 00 bb 01 c2 84 00 00 25 13 03 00 14 00 88 13 15 09 01 01 19 ff b8 1e 05 3f b8 1e 05 3f 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ed 85 ::: seq 187 sysid 1 compid 194 msgid DISTANCE_SENSOR crc 34285
~~~
