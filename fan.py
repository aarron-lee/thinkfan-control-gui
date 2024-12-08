#!/usr/bin/python3
import re
import subprocess
from time import sleep
from threading import Thread


'''
create a file called /etc/modprobe.d/thinkpad.conf that contains

options thinkpad_acpi fan_control=1

and to then reload the module

sudo modprobe -r thinkpad_acpi && sudo modprobe thinkpad_acpi

to check if speed level changed, you can check

cat /proc/acpi/ibm/fan
'''

def get_speed_level(avg_core_temp):
    if avg_core_temp <= 40.0:
        # fan off
        return 0
    elif avg_core_temp <= 50.0:
        return 1
    elif avg_core_temp <= 70.0:
        return 3
    elif avg_core_temp <= 80.0:
        return 5
    elif avg_core_temp <= 90.0:
        # max is 7
        return 7

    return 7

def get_info():
    info_lines = subprocess.check_output("sensors").decode("utf-8").split("\n")
    result = []
    temps = []
    count = 0
    for i in info_lines:
        if "Core" in i:
            result.append("Core %d: " % count + i.split(":")[-1].split("(")[0].strip())
            temps.append(i.split(":")[-1].split("(")[0].strip())
            count += 1

        if "fan" in i:
            result.append("Fan : " + i.split(":")[-1].strip())

    core_temps = [float(re.findall(r"[-+]?\d*\.\d+|\d+", item)[0]) for item in temps]
    avg_temp = sum(core_temps) / len(temps)

    output = {
        "avg_core_temp": avg_temp,
        "core_temps": core_temps,
        "info": result
    }

    return output

def set_speed(speed=None):
    """
    Set speed of fan by changing level at /proc/acpi/ibm/fan
    speed: 0-7, auto, disengaged, full-speed
    """
    print("set level to %r" % speed)
    return subprocess.check_output(
        'echo level {0} | sudo tee "/proc/acpi/ibm/fan"'.format(speed),
        shell=True
    ).decode()


if __name__ == "__main__":
    def display_loop():
        previous_speed = -1
        while True:
            sleep(2)
            fan_info = get_info()
            avg_core_temp = fan_info.get("avg_core_temp")

            speed = get_speed_level(avg_core_temp)

            if previous_speed != speed:
                set_speed(speed)
                print(f"Average Core Temp: {avg_core_temp} speed level: {speed}")
                print(f"speed changed from {previous_speed} to {speed}")
                previous_speed = speed
            #else:
            #    print(f"Average Core Temp: {avg_core_temp} speed level: {speed}")
            #    print(f"No speed change")

    Thread(target=display_loop).start()
