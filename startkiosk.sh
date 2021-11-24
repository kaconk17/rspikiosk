#!/bin/sh
xset -dpms      # disable DPMS (Energy Star) features.
xset s off      # disable screen saver
xset s noblank  # don't blank the video device
unclutter &     # hides your cursor after inactivity
i3 & # starts the WM
xterm &         # launches a helpful terminal
firefox --kiosk --noerrdialogs --disable-pinch --check-for-update-interval=604800 http://yourwebappaddress