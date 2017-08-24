#!/usr/bin/env python3

"""
modified from https://raw.githubusercontent.com/sarmbruster/thinkpad_x1_yoga_rotation/master/thinkpad_x1_yoga_rotation.py
changed to only handle disabling touchpad in tabled mode for X
Not running at startup because it doesn't behave properly if I switch to another tty (mouse just freezes and I have to kill X)
"""

#import dbus, sys, time, subprocess, socket, logging, docopt, multiprocessing, io, os, signal, atexit
import time, subprocess, socket, logging, multiprocessing, atexit
from gi.repository import GLib

name    = "thinkpad_x1_yoga_rotation"
version = "0.9-SNAPSHOT"


def cmd_and_log(cmd):
    exit = subprocess.call(cmd)
    log.info("running %s with exit code %s", cmd, exit)

# toggle trackpoint and touchpad when changing from laptop to tablet mode anc vice versa
def monitor_acpi_events(touch_and_track):
    socketACPI = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socketACPI.connect("/var/run/acpid.socket")

    is_laptop_mode = True
    log.info("connected to acpi socket %s", socket)
    #onboard_pid = None
    while True:
        event = socketACPI.recv(4096)
        log.debug("catching acpi event %s", event) 
        
        if event == b"video/tabletmode TBLT 0000008A 00000000\n":
            for x in touch_and_track:
                cmd_and_log(["xinput", "enable", x])
        elif event == b"video/tabletmode TBLT 0000008A 00000001\n":
            for x in touch_and_track:
                cmd_and_log(["xinput", "disable", x])

        #eventACPIDisplayPositionChange = "ibm/hotkey LEN0068:00 00000080 000060c0\n"
        # eventACPIDisplayPositionChange = b" PNP0C14:03 000000b0 00000000\n"
        #eventACPIDisplayPositionChange = b" PNP0C14:04 000000b0 00000000\n"
        #if event == eventACPIDisplayPositionChange:
        #    is_laptop_mode = not is_laptop_mode
        #    log.info("display position change detected, laptop mode %s", is_laptop_mode)
        #    if is_laptop_mode:
        #        for x in touch_and_track:
        #            cmd_and_log(["xinput", "enable", x])
        #        #log.info("onboard pid %s", onboard_pid)
        #        #if onboard_pid:
        #        #    log.info("stopping onboard")
        #        #    os.kill(onboard_pid, signal.SIGTERM)
        #    else:
        #        for x in touch_and_track:
        #            cmd_and_log(["xinput", "disable", x])
        #        #subprocess.call(["xinput", "--disable", "SynPS/2 Synaptics TouchPad"])
        #        #p = subprocess.Popen(['nohup', 'onboard'],
        #        #    stdout=open('/dev/null', 'w'),
        #        #    #stderr=open('logfile.log', 'a'),
        #        #    preexec_fn=os.setpgrp
        #        #) 
        #        #onboard_pid = p.pid
        #        #log.info("started onboard with pid %s", onboard_pid)
        time.sleep(0.3)


def cleanup(touch_and_track):
    for x in touch_and_track:
        cmd_and_log(["xinput", "enable", x])

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

    # load stylus touchpad trackpoint devices
    lines = subprocess.check_output(['xinput','--list', '--name-only']).decode().split('\n')

    # it's crucial to have trackpoints first in this list. Otherwise enabling/disabling doesn't work as expected and touchpad just stays enabled always
    touch_and_track = [x for x in lines if "TrackPoint" in x] + [x for x in lines if "TouchPad" in x]
    log.info("found touchpad and trackpoints %s", touch_and_track)

    # listen for ACPI events to detect switching between laptop/tablet mode
    acpi_process = multiprocessing.Process(target = monitor_acpi_events, args=(touch_and_track,))
    acpi_process.start()

    atexit.register(cleanup, touch_and_track)

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    #options = docopt.docopt(__doc__)
    #if options["--version"]:
    #    print(version)
    #    exit()
    main()
