#!/usr/bin/env python3

"""
NOTE: this is not needed in gnome, where rotation is handled automaticly
taken from https://github.com/sarmbruster/thinkpad_x1_yoga_rotation/blob/master/thinkpad_x1_yoga_rotation.py
modified to only do rotation
Usage:
    rotate.py [options]
Options:
    -h,--help        display help message
    --version        display version and exit
"""

import dbus, subprocess, logging, atexit
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

name    = "thinkpad_x1_yoga_rotation"
version = "0.9-SNAPSHOT"

# map sensor-proxy orientation to xrandr and wacom
xrandr_orientation_map = {
    'right-up': 'right',
    'normal' : 'normal',
    'bottom-up': 'inverted',
    'left-up': 'left'
}

wacom_orientation_map = {
    'right-up': 'cw',
    'normal' : 'none',
    'bottom-up': 'half',
    'left-up': 'ccw'
}

def cmd_and_log(cmd):
    exit = subprocess.call(cmd)
    log.info("running %s with exit code %s", cmd, exit)

def sensor_proxy_signal_handler(source, changedProperties, invalidatedProperties, **kwargs):
    if source=='net.hadess.SensorProxy':
        if 'AccelerometerOrientation' in changedProperties:
            orientation = changedProperties['AccelerometerOrientation']
            log.info("dbus signal indicates orientation change to %s", orientation)
            #subprocess.call(["xrandr", "-o", xrandr_orientation_map[orientation]])
            subprocess.call(["xrandr", "--output", "eDP1", "--rotate", xrandr_orientation_map[orientation]])
            for device in wacom:
                cmd_and_log(["xsetwacom", "--set", device, "rotate", wacom_orientation_map[orientation]])
            if orientation in ['bottom-up', 'normal']:
                subprocess.call(['multi_monitor_touch_fix.sh', 'h'])
            else:
                subprocess.call(['multi_monitor_touch_fix.sh', 'v'])


#def cleanup(touch_and_track, wacom):
def cleanup(wacom):
    #subprocess.call(["xrandr", "-o", "normal"])
    subprocess.call(["xrandr", "--output", "eDP1", "--rotate", "normal"])
    for device in wacom:
        cmd_and_log(["xsetwacom", "--set", device, "rotate", "none"])

def main():
    # logging
    global log
    log        = logging.getLogger()
    logHandler = logging.StreamHandler()
    log.addHandler(logHandler)
    logHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.level  = logging.INFO

    # load wacom devices 
    lines = subprocess.check_output(['xsetwacom','--list', 'devices']).split(b'\n')

    global wacom
    wacom = [ x.decode().split('\t')[0] for x in lines if x]
    log.info("detected wacom devices: %s", wacom)

    # load stylus touchpad trackpoint devices
    lines = subprocess.check_output(['xinput','--list', '--name-only']).decode().split('\n')

    stylus = next(x for x in lines if "stylus" in x)
    log.info("found stylus %s", stylus)

    finger_touch = next(x for x in lines if "Finger touch" in x)
    log.info("found finger touch %s", finger_touch)

    atexit.register(cleanup, wacom)

    # init dbus stuff and subscribe to events
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    proxy = bus.get_object('net.hadess.SensorProxy', '/net/hadess/SensorProxy')
    props = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    props.connect_to_signal('PropertiesChanged', sensor_proxy_signal_handler, sender_keyword='sender')
    iface = dbus.Interface(proxy, 'net.hadess.SensorProxy')
    iface.ClaimAccelerometer()
    #iface.ClaimLight()

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
