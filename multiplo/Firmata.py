
# Standard Library Imports
import logging
import time
import sys
import signal

# Third party imports
from PyMata.pymata import PyMata

# Local Imports
from NestedDict import NestedDict

class Firmata(NestedDict):

    board = None

    def __init__(self, *args):
        #NestedDict.__init__(self, args)
        NestedDict.__init__(self)

        self.logger = logging.getLogger(self.__class__.__name__)

        if Firmata.board is None: 
            signal.signal(signal.SIGINT, Firmata.signal_handler)
            Firmata.board = PyMata(self.setdefault("usb_port", "/dev/ttyACM0"))
            self.logger.info("Initialized firmata board '%s'", self["usb_port"]);

    def __del__(self):
        if Firmata.board is not None:
            Firmata.board.reset()
            Firmata.board = None

    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!!!!')
        if Firmata.board is not None:
            Firmata.board.reset()
            Firmata.board = None

    def on_message(self, mqtt, xxx,  obj, msg):
        cmds = msg.topic.split("/")
        self.logger.info("Msg: %s - %s", cmds[1], cmds[2])

        if (cmds[1] == "SYSEX_QUERY" ):
            if (cmds[2] == "DIGITAL_PINS"):
                mqtt.mos.publish(cmds[0] + "/SYSEX_RESPONSE/DIGITAL_PINS", 5, 0) 
        


if __name__ == '__main__':
    firmata =  Firmata()

    # digital pin 13 is connected to an LED
    BOARD_LED = 13

    BOARD_BAT = 6

    count = 0


    # set digital pin 13 to be an output port
    firmata.board.set_pin_mode(BOARD_LED, firmata.board.OUTPUT, firmata.board.DIGITAL)

    firmata.board.set_pin_mode(BOARD_BAT, firmata.board.INPUT, firmata.board.ANALOG)
    firmata.board.set_analog_latch(BOARD_BAT, firmata.board.ANALOG_LATCH_GTE, 1000)

    time.sleep(5)
    print("Blinking LED on pin 13")

    #  blink for 10 times
    for x in range(10):
        print(x + 1)
        firmata.board.digital_write(BOARD_LED, 1)
        #  wait a half second between toggles.
        time.sleep(.2)
        firmata.board.digital_write(BOARD_LED, 0)
        time.sleep(.2)

    while count<10:
        count += 1
        analog = firmata.board.analog_read(BOARD_BAT)
        print('Battery: ' )
        print(analog)

    # close PyMata when we are done
    #firmata.close()
