#!/bin/bash
TOTAL_WIDTH=$(xdpyinfo | grep dimensions | sed 's/dimensions:\s*\([0-9]*\)x[0-9].*/\1/')



if [ $1 = "h" ]; then
        HORIZ_FRAC=$(echo 2560./$TOTAL_WIDTH | bc -l)
elif [ $1 = "v" ]; then
        HORIZ_FRAC=$(echo 1440./$TOTAL_WIDTH | bc -l)
else
        echo "Bad argurment!"
fi

#default_IFS=$IFS
#IFS="$(echo -e "\n\r")"
#for device in $(xinput --list --name-only | grep Wacom); do            #NO IDEA WHY THIS DOESN'T WORK
for device in 9  10  17; do
     xinput set-prop $device --type=float "Coordinate Transformation Matrix" $HORIZ_FRAC 0 0 0 1 0 0 0 1
done
#IFS=$default_IFS
