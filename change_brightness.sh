#!/bin/zsh


# Returns the floating point software brightness.
function get_xrandr_brightness ()
{
    echo $(xrandr --current --verbose | grep Brightness) | grep -o -E "[-+]?[0-9]*\.?[0-9]+"

}

SOFT_BRIGHTNESS=$(get_xrandr_brightness)

# Increases software brightness linearly.
function increase_software_brightness ()
{
    xrandr --output eDP1 --brightness $(($SOFT_BRIGHTNESS+.2))
}

# Decreases software brightness linearly.
function decrease_software_brightness ()
{
    xrandr --output eDP1 --brightness $(($SOFT_BRIGHTNESS-.2))
}



if [ $1 = "up" ]; then
    if [ 1 -eq $(($SOFT_BRIGHTNESS > 0.9)) ]; then
        xrandr --output eDP1 --brightness 1.0
    else
        increase_software_brightness
    fi
elif [ $1 = "down" ]; then
    if [ 1 -eq $(($SOFT_BRIGHTNESS < 0.3)) ]; then
        xrandr --output eDP1 --brightness 0.0
    else
        decrease_software_brightness
    fi
else
    echo "Unsupported operator!"
fi

