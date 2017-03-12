# rpi-status-mqtt
Rasperry PI status CPU , RAM, Disk

You will need Python 2.7 pip to be installed

```bash
sudo apt install python-pip
```

Also Paho MQTT library

```bash
 pip install paho-mqtt
```

Run it using cron

```cron
 */1 * * * * /usr/bin/python /home/pi/rpi-status/stats.py >/dev/null 2>&1
 ```