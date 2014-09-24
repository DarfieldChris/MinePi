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
import paho.mqtt.client as paho

#Local Application/Library Specific Imports
import config
import gpio

class mqtt:
    """Class to connect/communicate with MQTT server"""

    on_message_obj = None

    def __init__(self, cfg):
        """Class Constructor ... called when object instance created.
    
           Arguments:
               self - object being created
               cfg  - pointer to config.YAMLConfig class instance
        """

        self.cfg = cfg

        # Figure out the details of the MQTT Server to talk to
        self.uri = cfg.get("Mqtt", "Server", default = "localhost") 
        self.port = cfg.get("Mqtt", "Port", default = "1883")
        self.ident = cfg.get("Mqtt", "Identity", default = "xxx")
        #self.topicheader = topicheader+ '/' + self.ident
        self.topicheader = cfg.get("Mqtt", "Topic", default = "xxx")

        self.outputRegex = re.compile(self.topicheader + "/output/(\d*)", re.IGNORECASE)

	logging.info("Listening for MQQT messages:  %s/output/(\d*)", self.topicheader)
        
        # setup as MQQT client
        self.mos = paho.Client(self.ident)
        self.mos.on_connect = self.on_connect
        self.mos.on_disconnect = self.on_disconnect
        self.mos.on_message = self.on_message # register for callback

        while (self.connect() == False ):
            logging.info ("Trying to connect again ...")
            time.sleep(5)
        
    #
    # Method: connect
    #
    # Connect to MQTT server
    #
    # Arguments:
    #    self - pointer to self
    #
    def connect(self, reconnect = False):
        try:
            if (reconnect):
                self.mos.reconnect()
            else:
                self.mos.connect(self.uri, port=self.port)
        except:
            e = sys.exc_info()[0]
            logging.warning("Connection Failed with error: %s", str(e))
            #raise
            return False
        logging.info("connected to mqtt server at %s:%d", self.uri, self.port)
        return True
    
    #
    # Method: run
    #
    # Continuous loop to check status of Pi Inputs and report changes back to 
    # minecraft server
    #
    # Arguments:
    #    self - pointer to self
    #
    def run(self):
        while self.mos.loop(10000) == 0:
            logging.info("mqtt.run: Woke up ...")
            #self.triggerOutputs(98, True)

    # The callback for when the client receives a CONNACK response
    # from the server.
    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code: %s", str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.mos.subscribe(self.topicheader + "/output/+", 0) # get all messages for me
        #self.mos.subscribe("#", 0) # get all messages
        logging.info("subscribed to %s/output/+", self.topicheader)

    def on_disconnect(self, userdata, flags, rc):
        if (rc):    # unexpected disconnection ... try to reconnect
            logging.warning("Disconnected with result code: %s", str(rc))

            logging.info("Trying to reconnect ...")
            while (self.connect(True) == False ):
                logging.info ("Failed to reconnect.  Will sleep and try again ...")
                time.sleep(5)
 
    #
    # Method: on_message
    #
    # callback method executed when message received from MQTT server
    #
    # Arguments:
    #    self - pointer to self
    #    obj - ???
    #    msg - ???
    #
    def on_message(self, xxx,  obj, msg):
        logging.info("Msg received: %s - %s", msg.topic, msg.payload)
        
        rm = self.outputRegex.match( msg.topic )
        
        if rm != None:
            if ( self.on_message_obj != None):
                self.on_message_obj.trigger (rm.group(1), msg.payload)
                

        logging.debug("on_message: Finished")


    def __del__(self):
        self.mos.disconnect()

#
# MAIN CODE - THIS IS WHAT IS RUN IF YOU TYPE 'python pfmqtt.py' in a shell
#
if __name__ == '__main__':
    # set default logging level prior to parsing config info
    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

    # read config file
    cfg = config.YAMLConfig()
    cfg.setLogging()

    conn = mqtt(cfg)
    io = gpio.gpio(cfg, conn)
    conn.on_message_obj = io

    while (True):
        conn.run()

    logging.info("Finished normally")
