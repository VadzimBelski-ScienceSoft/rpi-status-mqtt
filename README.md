# rpi-status-mqtt
Rasperry PI status CPU , RAM, Disk

You will need Python 2.7

Also Paho MQTT library
`` pip install paho-mqtt

Run it using cron

`` */1 * * * * /usr/bin/python /home/pi/rpi-status/stats.py >/dev/null 2>&1