import imp
import LPS25HB
from time import sleep

sleep(0.1)
if (LPS25HB.LPS_init() == False):
    print("Failed to autodetect pressure sensor!")
    while (True):
        sleep(0.1)

LPS25HB.enableDefault()
while(True):
    pressure = LPS25HB.readPressureMillibars()
    altitude = LPS25HB.pressureToAltitudeMeters(pressure)
    temperature = LPS25HB.readTemperatureC()

    print("p:", round(pressure, 2), "tmbar a:", round(
        altitude, 2), "mttt:", round(temperature, 2), "deg C ")
    sleep(0.1)