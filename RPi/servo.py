#
# Notes: 
#     Frequency of:
#         50 hz = 20 milliseconds
#         25 hz = 40 milliseconds
#
#     Want a cycle of 40 ms so will start with 25 hz ...
#
#     With a 25 hz frequency (40 ms duration) need the following 
#     duty cycles:
#     High Duration % of total cycle     Direction
#     ============= ================     =========
#         1 ms      1/40X100 = 2.5 %     left
#         2 ms      2/40x100 = 5 %       right
#         1.5 ms    1.5/40x100=3.75 %    centre
#

# Standard Library Imports
import time
import sys
import logging

# Third Party Imports
import RPi.GPIO as GPIO

# Local Application/Library Specific Imports
import config

class servo:

    def __init__(self, pin, cont = False):
        self.pos=.0015
        self.pin = pin
        self.cont = cont

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin,0)

        if (self.cont == False) :
            self.__move(self.pos)

    def __move (self, high = 0.0015, low = 0.0400, cycles=1):
        for x in range (0, cycles):
            GPIO.output(self.pin,1)
            time.sleep(high)
            GPIO.output(self.pin,0)
            time.sleep(low)
        logging.debug("__move: %f", high);  

    def __move2 (self, steps = .0001, min = .001, max = .002):

         if (steps == 0):
             self.pos = .0015
             self.__move(self.pos)
         else:
             self.pos += steps

         if (self.pos < min):
             self.pos = min
         elif (self.pos > max):
             self.pos = max

         self.__move(self.pos)

    def move (self, steps = .0001, min = .0006, max = .0022):
        if (self.cont == True):
            if (steps > 0):
                self.__move(.001)
            elif (steps == 0):
                self.__move(.0015)
            else:
                self.__move(.0020)
        else:
            self.__move2(steps, min, max)

if __name__=='__main__':
    # set default logging level prior to parsing config info
    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

    # read config file and set logging level based on value in config file
    cfg = config.YAMLConfig()
    cfg.setLogging()

    GPIO.setmode(GPIO.BCM)
    pan = servo(7, False)
    tilt = servo(8, True)

    try:
        while True:
            c = sys.stdin.read(1)
            print "got a ... " + c
            if ( c == "a"):
                pan.move(.0001)
            elif ( c == "d"):
                pan.move(-.0001)
            elif ( c == "s"):
                pan.move(0)
            elif ( c == "j"):
                tilt.move(.0001)
            elif (c == "k"):
                tilt.move(0)
            elif (c == "l"):
                tilt.move(-.0001)

    except KeyboardInterrupt:
        GPIO.cleanup()
