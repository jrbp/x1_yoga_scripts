#!/bin/bash
TOTAL_WIDTH=$(xrandr -q | grep Screen | sed "s/Screen.*current\s\([0-9]*\)\sx\s[0-9]*,.*/\1/")
TOTAL_HEIGHT=$(xrandr -q | grep Screen | sed "s/Screen.*current\s[0-9]*\sx\s\([0-9]*\),.*/\1/")

res_x=$(xrandr -q | grep eDP1 | sed "s/.*[yd]\s\([0-9]*\)x[0-9]*\+[0-9]*\+[0-9]*.*/\1/")
res_y=$(xrandr -q | grep eDP1 | sed "s/.*[yd]\s[0-9]*x\([0-9]*\)\+[0-9]*\+[0-9]*.*/\1/")
offset_x=$(xrandr -q | grep eDP1 | sed "s/.*[yd]\s[0-9]*x[0-9]*+\([0-9]*\)+[0-9]*.*/\1/")
offset_y=$(xrandr -q | grep eDP1 | sed "s/.*[yd]\s[0-9]*x[0-9]*+[0-9]*+\([0-9]*\).*/\1/")

c0=$(echo $res_x/$TOTAL_WIDTH | bc -l)
c2=$(echo $res_y/$TOTAL_HEIGHT | bc -l)
c1=$(echo $offset_x/$TOTAL_WIDTH | bc -l)
c3=$(echo $offset_y/$TOTAL_HEIGHT | bc -l)

#default_IFS=$IFS
#IFS="$(echo -e "\n\r")"
#for device in $(xinput --list --name-only | grep Wacom); do            #NO IDEA WHY THIS DOESN'T WORK
for device in 9  10  17; do
     xinput set-prop $device --type=float "Coordinate Transformation Matrix" $c0 0 $c1 0 $c2 $c3 0 0 1
done
#IFS=$default_IFS
