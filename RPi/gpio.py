"""MQTT script run on raspberry Pi."""
#! /usr/bin/python

# Notes:
# 
# To install python/mosquitto library run following line in shell
# (this assumes you have your piface installed and the python library 
#  installed too)
#
#apt-get install python-mosquitto

#Standard Library Imports
import sys
import time
import os
import logging
import re

#Third Party Imports
import RPi.GPIO as GPIO

#Local Application/Library Specific Imports
import config
import camera
import servo

class gpio:
    """Class to control GPIO on Pi"""

    def __init__(self, cfg, mqtt_client = None):
        """Class Constructor ... called when object instance created.
    
           Arguments:
               self - object being created
               cfg  - pointer to config.YAMLConfig class instance
        """

        self.mqtt_client = mqtt_client
        
        self.cfg = cfg

        # setup RPi GPIO
        #    set up GPIO using BCM numbering
        GPIO.setmode(GPIO.BCM)

        self.motors = {}

        for pin in cfg.get("Pins"):
            if (cfg.get("Pins", pin, "type") == "IN"):
                GPIO.setup(pin, GPIO.IN, 
                           pull_up_down = getattr(GPIO, cfg.get("Pins",pin,"pull_up_down")))
                GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.inputStateChange, 
                                      bouncetime=100)
            elif (cfg.get("Pins", pin, "type") == "OUT"):
                GPIO.setup(pin, GPIO.OUT)
	        GPIO.output(pin, True)
                time.sleep(1)
                GPIO.output(pin,False)
            elif (cfg.get("Pins",pin,"type") == "SERVO"):
                self.motors[pin] = servo.servo(pin, cfg.getBoolean("Pins",pin,"continuous"))

            logging.info("Setting up pin %d as %s", pin, cfg.get("Pins", pin, "type"))
        
    def inputStateChange(self, channel):
        """Called when state change detected on GPIO input pin.

           Arguments:
               channel (int) - the GPIO channel for which the state changed.
        """

        #GPIO.remove_event_detect(channel)

        # send out an MQTT message about the state change
        self.publish(channel, str(GPIO.input(channel)))
            
        logging.info("Button state changed ... pin %d reading %s", channel,str(GPIO.input(channel)))

        # check to see if there are any triggers 
        trigger = self.cfg.get("Pins",channel,"trigger", default = None)
        if (trigger):
            logging.debug("inputStateChange: Processing trigger %s", trigger)
            self.triggerOutputs(int(trigger), GPIO.input(channel))
            logging.debug("inputStateChange: Processed trigger")

        #GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.inputStateChange, bouncetime=100)

    def trigger(self, strPin, payload):
        iPayLoad = 0
        pin = int(strPin)
            
        if payload == '0':
	    iPayLoad = 0
        else:
	    iPayLoad = 1

        self.triggerOutputs(pin, iPayLoad)

        # check to see if there are any triggers on this pin
        trigger = self.cfg.get("Pins",pin,"trigger", default = None)
        if (trigger):
            logging.debug("on_message: Processing trigger %s", trigger)
            self.triggerOutputs(int(trigger), iPayLoad)
            logging.debug("on_message: Processed trigger")

    def triggerOutputs(self, pin, high_low):
            if (self.cfg.get("Pins", pin, "type") == "OUT"):
                logging.info("setting pin %d to %d", pin, high_low)
                GPIO.output(pin, state)
            elif (self.cfg.get("Pins", pin, "type") == "camera_ssh" and high_low):
                self.__take_pic(pin, ssh=True)
 
            elif (self.cfg.get("Pins", pin, "type") == "camera" and  high_low):
                #logging.debug("YES")
                self.__take_pic(pin)
                #logging.debug("NO")
          
            elif (self.cfg.get("Pins",pin,"type") == "cameraPanPositive" and high_low):
                servo_pin = int(self.cfg.get("Pins",pin,"servo"))
                self.motors[servo_pin].move(0.0001)
            elif (self.cfg.get("Pins",pin,"type") == "cameraPanNegative" and high_low):
                servo_pin = int(self.cfg.get("Pins",pin,"servo"))
                self.motors[servo_pin].move(-0.0001)
            #logging.debug("NO2")



    def __take_pic(self, pin, ssh = False):
        logging.info("Taking picture ...")
        cam = camera.Camera (self.cfg, self.cfg.get("Pins", pin, "camera"))
        cam.takePicture()


        # send a message back indicating a picture has been taken ...
        if (ssh):
            logging.info("... and returning image via HTTP")
            cam.forwardSSHServer(self.cfg.get("Pins",pin,"camera_dest"))

            img = cam.strRemotePath
            img = os.path.basename(img)
            self.publish( pin, img)
        else: 
            #byteArray = cam.getString()
            byteArray = cam.getByteArray()
            logging.info("... and returning binary image message - %d.", len(byteArray))
            self.publish(pin, byteArray)

    def publish(self,pin,message):
        if (self.mqtt_client != None):
            logging.info("gpio  publication: %d", pin)
            self.mqtt_client.mos.publish( self.mqtt_client.topicheader + '/input/pin' + str(pin),
                                          message, 0 )

    def __del__(self):
        GPIO.cleanup()

#
# MAIN CODE - THIS IS WHAT IS RUN IF YOU TYPE 'python pfmqtt.py' in a shell
#
if __name__ == '__main__':
    # set default logging level prior to parsing config info
    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

    # read config file
    cfg = config.YAMLConfig()
    cfg.setLogging()

    io = gpio(cfg)
    
    logging.info("Finished normally")
