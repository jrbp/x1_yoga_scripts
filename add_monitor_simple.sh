#!/bin/bash
#currently only puts the monitor to the right and only on HDMI

xrandr --output HDMI1 --auto --right-of eDP1
multi_monitor_touch_fix.sh
