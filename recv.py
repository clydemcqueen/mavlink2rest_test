#!/usr/bin/env python3

from tlog_bad_data import BadDataInfo
from pymavlink import mavutil


# TODO send a heartbeat?

conn = mavutil.mavlink_connection('udpin:0.0.0.0:14550', source_system=254, source_component=0)

num_distance_sensor_msgs = 0
num_bad_data_msgs = 0

while True:
    # It appears that I can't filter for BAD_DATA messages, so get them all
    msg = conn.recv_match(blocking=True)

    msg_type = msg.get_type()

    if msg_type == 'DISTANCE_SENSOR':
        num_distance_sensor_msgs += 1
        if num_distance_sensor_msgs % 100 == 0:
            print(f'{num_distance_sensor_msgs} DISTANCE_SENSOR msgs, {num_bad_data_msgs} BAD_DATA msgs')

        # timestamp = getattr(msg, '_timestamp', 0.0)
        # crc = msg.get_crc()
        # sys_id = msg.get_srcSystem()
        # comp_id = msg.get_srcComponent()
        # data = msg.to_dict()

        # crc_extra is per-message, defined by mavgen
        # The sender and receiver should have the same crc_extra value for that message type
        # https://mavlink.io/en/guide/serialization.html#crc_extra
        # crc_extra = msg.crc_extra

        # print(f'time {timestamp} crc {crc} crc_extra {crc_extra}')

    elif msg_type == 'BAD_DATA':
        print('=================== BAD DATA ==================')
        print(BadDataInfo(msg))
        num_bad_data_msgs += 1
