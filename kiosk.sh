
export DISPLAY=:0
xset s noblank
xset s off
xset -dpms
unclutter -idle 0.5 -root &
/usr/bin/python3 /home/pi/temp_flask/temp_flask.py &
sleep 5
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk --app=http://0.0.0.0:5000/

