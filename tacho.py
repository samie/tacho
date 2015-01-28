#!/usr/bin/python

import sys
import math
import time
import psutil
import atexit
import RPi.GPIO as GPIO

# Hz calibration vector for values 0-10 (x1000 RPM)
steps = [34,118,206,285,373,453,543,647,793]
#calibration hz values = [0, 18,6,-15,-27,-47,-57,-53,-7,-100,-200]

maxValue = 8
minValue = 0
duty_cycle = 10
gpio_channel = 11
p = 0

def gpioCleanup():
   GPIO.cleanup()

def tohz(value):

   # keep us on scale
   if value > maxValue:
       value = maxValue;
   if value < minValue:
       value = minValue

   # linear interpolation
   x0 = int(math.floor(value))   
   x1 = int(math.ceil(value))   
   if x0 == x1: 
      hz = steps[x0]
   else:
       hz0 = steps[x0]
       hz1 = steps[x1]
       hz = hz0 + (hz1 - hz0)*(value-x0)/(x1-x0)
   return hz

def stop():
    global p
    p.stop()

def start():
    global p
    if p == 0:
        p = GPIO.PWM(gpio_channel,1)
    p.start(duty_cycle)

def setValue(value):
    global p
    x = float(value)
    hz = tohz(x)
    if not quiet:
        print 'Set to %f = %dHz ' % (x, hz)
    p.ChangeFrequency(hz)

def testLimits():
    print 'Test max...'
    setValue(maxValue)
    time.sleep(2)
    print 'done.'
    print 'Test min...'
    setValue(0)
    time.sleep(2)
    print 'done.'


def testScale(reverse = False):
    print 'Scale test...'
    r = range(1,9)
    if reverse:
       r = reversed(r)   
    for x in r:
       setValue(x)
       time.sleep(1)
    print 'done.'

def cpuInfo():
    print 'Showing CPU status...'
    while (True):
       cpu = psutil.cpu_percent()
       setValue(cpu/10)
       time.sleep(1)

def networkInfo():
    print 'Showing network status (M/s)...'
    while (True):
       nwBefore = psutil.net_io_counters()
       time.sleep(1)
       nwAfter = psutil.net_io_counters()
       setValue(float(nwAfter.bytes_recv - nwBefore.bytes_recv)/ float(1000000))

def main(argv):
    if 'test' == argv[1]:
        start()
        testLimits()
        testScale()
        testScale(True)
        stop()
    elif 'cpu' == argv[1]:
         start()
         cpuInfo()
    elif 'network' == argv[1]:
         start()
         networkInfo()
    elif len(argv) > 1:
         start()
         setValue(argv[1])
         time.sleep(5)
         stop
    else:
         print 'Usage: %s [test|cpu|network] [quiet]' % argv[0]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
atexit.register(gpioCleanup)
quiet = len(sys.argv) > 2 and sys.argv[2] == "quiet"
main(sys.argv)
