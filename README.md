# alearn

This use adb to manipulate android app "Learn to strong" automatically.
Tested under Ubuntu 18.04, Openwrt 18.06.

Requirements:
apt install adb
apt install python3

Using crontab to run daily:
0 20 * * * /root/cron.sh >/dev/null 2>&1
