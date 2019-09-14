cd /home/pi/temperature

export DISPLAY=:0
xset s noblank
xset s off
xset -dpms
unclutter -idle 0.5 -root &
/usr/bin/python3 /home/pi/temperature/collect.py &
/usr/bin/python3 /home/pi/temperature/server.py &
sleep 5
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk --app=http://192.168.1.189:8050/

