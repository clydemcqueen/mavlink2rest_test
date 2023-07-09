#!/usr/bin/env python3

import asyncio
import time

from commonwealth.mavlink_comm.exceptions import MavlinkMessageSendFail
from ping1d_mavlink import Ping1DMavlinkDriver


def main():
    mavlink_driver = Ping1DMavlinkDriver(False)

    while True:
        try:
            asyncio.run(mavlink_driver.send_distance_data(333, 444, 0))
        except MavlinkMessageSendFail as e:
            print(e)

        time.sleep(1.0)


main()
