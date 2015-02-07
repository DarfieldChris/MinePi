import sys
import serial
import time
import fcntl
import os

def setNonBlocking(fd): 
    """Make a fd non-blocking.""" 
    flags = fcntl.fcntl(fd, fcntl.F_GETFL) 
    flags = flags | os.O_NONBLOCK 
    fcntl.fcntl(fd, fcntl.F_SETFL, flags) 

#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/ttyAMA0', 9600)
setNonBlocking(ser)

try:
    while True:
        c = sys.stdin.read(1)
        if (c >= '0' and c <= '9'):
            print "STDIN: got a ... '" + c + "' ... forwarding it to the Pi"
            ser.write(c)

        time.sleep(1)

        #for line in ser:
        #    print "SERIAL: got ... " + line

except KeyboardInterrupt:
    GPIO.cleanup()

