from adbcmd import adbcmd
from random import random as rnd
import time
from mailpng import mailpng
from autogui import locateAll
from PIL import Image

ADB = adbcmd('F8UDU15519010985')


def UIDelay():
    time.sleep(4+rnd())

def LDelay(isVideo):
	if isVideo:
	    return 180+rnd()
	else:
		return 120+rnd()

def subLearn(x, y, duration):
	ADB.short_tap((x, y))
	time.sleep(duration)
	ADB.key("KEYCODE_BACK")
	UIDelay()	

def findAndLearn(tms, duration):
	i = 0
	imgYear = Image.open('year.png')
	swipe = 0
	while i<tms:
		imgScreen = ADB.screencapImg()
		# imgScreen.save('temp.png')
		for x, y, w, h in locateAll(imgYear, imgScreen):
			subLearn(x, y+10, duration)
			i+=1
		if i==0 and swipe>1: ## can't find it within 2 pages
			return
		if i<tms:
			ADB.swipe((500, 1500, 500, 500), 1000)
			swipe += 1
			UIDelay()

def Learn():
	# switch to 'learn'
	ADB.short_tap((540, 1730))
	UIDelay()
	# //switch to recommend
	ADB.short_tap((120, 280))
	UIDelay()
	
	findAndLearn(6, LDelay(False))

def Vido():
	# //switch to 'video'
	ADB.short_tap((760, 1730))
	UIDelay()
	# //switch to 1st
	ADB.short_tap((160, 280))
	UIDelay()
	
	findAndLearn(3, LDelay(True))

	# //Switch lianbo
	ADB.short_tap((600, 280))
	UIDelay()
	ADB.short_tap((600, 280))
	UIDelay()
	findAndLearn(3, LDelay(True))

def DailyLearn():
	if ADB.get_batterylevel()<50:
		ADB.enable_charger(True)

	time.sleep(60*rnd())
	ADB.unlock()
	
	# //launch app
	ADB.startApp('cn.xuexi.android/com.alibaba.android.rimet.biz.SplashActivity')
	time.sleep(30)
	
	Learn()
	Vido()

	ADB.short_tap((780, 146))
	UIDelay()
	ADB.screencap('screenshot.png')
	mailpng('screenshot.png', ['mice2100@163.com', 'opticmcu@gmail.com'])

	ADB.key("KEYCODE_BACK")
	UIDelay()
	ADB.key("KEYCODE_HOME")
	UIDelay()
	
	ADB.lock()
	ADB.enable_charger(False)
	
if __name__ == "__main__":
    DailyLearn()
	# ADB.screencap('screenshot.png')
