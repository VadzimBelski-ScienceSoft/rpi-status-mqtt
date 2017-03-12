import os
import paho.mqtt.client as mqtt

mqttc = mqtt.Client("rpi-status"+ os.uname()[1])

mqttc.username_pw_set("<USER NAME>","<PASSWORD>")
mqttc.connect("<IP>", 1883)

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    # retrieves information for the harddrive where root is mounted
    # in windows replace this with "C:\" or the relevant drive letter
    disk = os.statvfs("/")

    # Information is recieved in numbers of blocks free
    # so we need to multiply by the block size to get the space free in bytes
    capacity = disk.f_bsize * disk.f_blocks
    available = disk.f_bsize * disk.f_bavail
    used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)

    # # print information in Kilobytes
    # print used / 1024, available / 1024, capacity / 1024
    #
    # # print information in Megabytes
    # print used / 1.048576e6, available / 1.048576e6, capacity / 1.048576e6
    #
    # # print information in Gigabytes
    # print used / 1.073741824e9, available / 1.073741824e9, capacity / 1.073741824e9

    # print information in bytes
    return used / 1.048576e6, available / 1.048576e6, capacity / 1.048576e6



# CPU informatiom
CPU_temp = getCPUtemperature()
CPU_usage = getCPUuse()

# RAM information
# Output is in kb, here I convert it in Mb for readability
RAM_stats = getRAMinfo()
RAM_total = round(int(RAM_stats[0]) / 1000,1)
RAM_used = round(int(RAM_stats[1]) / 1000,1)
RAM_free = round(int(RAM_stats[2]) / 1000,1)

# Disk information
DISK_stats = getDiskSpace()
DISK_total = DISK_stats[2]
DISK_free = DISK_stats[1]
DISK_perc = DISK_stats[0]

topic_base = "home/rpi/"
topic = topic_base + os.uname()[1] + "/"

print topic

# Pubish to MQTT

mqttc.publish(topic + 'cpu_temp', CPU_temp )
mqttc.publish(topic + 'cpu_usage', CPU_usage )


mqttc.publish(topic + 'ram_total', RAM_total )
mqttc.publish(topic + 'ram_used', RAM_used )
mqttc.publish(topic + 'ram_free', RAM_free )

mqttc.publish(topic + 'disk_total', DISK_total )
mqttc.publish(topic + 'disk_free', DISK_free )
mqttc.publish(topic + 'disk_perc', DISK_perc )

mqttc.publish
mqttc.loop(2)
