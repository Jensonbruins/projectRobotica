from __future__ import print_function
import time, sys, signal, atexit, math
try:
    from upm import pyupm_bmm150 as sensorObj
except ImportError:
    print('Error: Please install python-mraa python-upm module.\r\n'
          'See instruction here https://github.com/Seeed-Studio/pi_repo#mraa--upm-package-repository-for-raspberry-pi ')


class Kompas:
    def __init__(self):
        self.sensor = sensorObj.BMM150(0, 0x13)

    def lees_richting(self):
        self.sensor.update()
        data = self.sensor.getMagnetometer()
        xyRichting = math.atan2(data[0], data[1])
        richting = xyRichting

        if richting < 0:
            richting += 2 * math.pi
        if richting > 2 * math.pi:
            richting -= 2 * math.pi

        richtingGraden = richting * 180 / (math.pi)

        return richtingGraden
