#!/usr/bin/env python3

import asyncio
import random
import time

from commonwealth.mavlink_comm.exceptions import MavlinkMessageSendFail
from ping1d_mavlink import Ping1DMavlinkDriver


def main():
    mavlink_driver = Ping1DMavlinkDriver(False)

    while True:
        distance_mm = random.randrange(200, 50000)
        confidence = random.randrange(0, 100)

        try:
            asyncio.run(mavlink_driver.send_distance_data(distance_mm, 1, confidence))
        except MavlinkMessageSendFail as e:
            print(e)

        time.sleep(0.1)


main()
