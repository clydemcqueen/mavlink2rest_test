#!/usr/bin/env python3

from tlog_bad_data import BadDataInfo
from pymavlink import mavutil


# TODO send a heartbeat?

conn = mavutil.mavlink_connection('udpin:0.0.0.0:14550', source_system=254, source_component=0)

num_distance_sensor_msgs = 0
num_bad_data_msgs = 0

while True:
    msg = conn.recv_match(blocking=True)

    timestamp = getattr(msg, '_timestamp', 0.0)
    seq = msg.get_seq()
    sysid = msg.get_srcSystem()
    compid = msg.get_srcComponent()
    msgid = msg.get_type()
    data = msg.to_dict()
    crc = msg.get_crc()

    # crc_extra is per-message, defined by mavgen
    # The sender and receiver should have the same crc_extra value for that message type
    # https://mavlink.io/en/guide/serialization.html#crc_extra
    crc_extra = msg.crc_extra

    print(f'time {timestamp} seq {seq} sysid {sysid} compid {compid} msgid {msgid} crc {crc} crc_extra {crc_extra} data {data}')
