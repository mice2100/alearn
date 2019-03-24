from adbcmd import adbcmd
from random import random as rnd
import time
from mailpng import mailpng

ADB = adbcmd('F8UDU15519010985')


def UIDelay():
    time.sleep(2+rnd())

def LDelay():
    time.sleep(60+rnd())

def VDelay():
    time.sleep(300+60*rnd())

def LOp():
	x = int(rnd()*800)
	y = int(rnd()*400+1000)
	ADB.swipe((x, y, x, y-700))

def subLearn(x, y):
	ADB.short_tap((x, y))
	for i in range(4):
		LDelay()
		LOp()
	ADB.key("KEYCODE_BACK")
	UIDelay()	

def Learn():
	# switch to 'learn'
	ADB.short_tap((540, 1730))
	UIDelay()
	
	# //switch to headline
	ADB.short_tap((260, 280))
	UIDelay()
	
	subLearn(300, 500)
	subLearn(300, 900)
	subLearn(300, 1300)
	
	# //switch to bullshit
	ADB.short_tap((450, 280))
	UIDelay()
	
	subLearn(300, 650)
	subLearn(300, 1000)
	subLearn(300, 1500)

def Vido():
	# //switch to 'video'
	ADB.short_tap((800, 1730))
	UIDelay()
	
	# //switch to 1st
	ADB.short_tap((160, 280))
	UIDelay()
	ADB.short_tap((300, 500))
	VDelay()
	
	# //Switch short video
	ADB.short_tap((400, 280))
	UIDelay() 
	
	# //switch learn channel
	ADB.short_tap((180, 430))
	UIDelay() 
	ADB.short_tap((300, 700))
	VDelay()

	# //switch 2 channel
	ADB.short_tap((480, 430))
	UIDelay() 
	ADB.short_tap((300, 700))
	VDelay() 
	
	# //switch 3 channel
	ADB.short_tap((800, 430))
	UIDelay() 
	ADB.short_tap((300, 700))
	VDelay()

	# //Switch lianbo
	ADB.short_tap((600, 280))
	UIDelay()
	ADB.short_tap((300, 500))
	VDelay()

def DailyLearn():
	time.sleep(1200*rnd())
	ADB.unlock()

	ADB.key("KEYCODE_HOME")
	UIDelay()
	ADB.key("KEYCODE_HOME")
	UIDelay()
	
	ADB.swipe(( 700, 100, 300, 100))
	UIDelay()
	
	# //launch app
	ADB.short_tap((400, 500))
	time.sleep(8)
	
	Learn()
	Vido()

	ADB.screencap('screenshot.png')
	mailpng('screenshot.png')
	
	ADB.lock()
	
if __name__ == "__main__":
    DailyLearn()
