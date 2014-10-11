"""Module for capturing an image (a picture) from a web-based camera"""

#Standard Library Imports
from array import array
import io
import logging
import sys
import os
import subprocess

# Third Party Imports
import urllib
import paramiko
import picamera
if 0: # SimpleCV is HUGE ... ONLY IMPORT IF REQUIRED
   from SimpleCV.ImageClass import Image
   from SimpleCV import Camera

# Local Application/Library Specific Imports
import config

class MyCamera:
    """Class to download images from an http enabled or USB camera
    (so could actually be any web server)"""

    _cam = None

    def __init__(self, cfg, strCamera = "basic"):
        """Create an instance of this class.

           Arguments:
               strCamera - The key identifying the camera to use, 
                           this camera must be defined in the config file.
                           This key will be resolved to
                           'cameras.' + strCamera (e.g. cameras.dads_camera)
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.cfg_root = cfg
        self.cfg = cfg["cameras"][strCamera]
        self.cfg.setdefault("local_path", "./images/shot.jpg")
        self.cfg.setdefault("no_pic", "./images/xxx.jpg")
        self.cfg.setdefault("uri", None)

        if (self.cfg["uri"] == "PICAMERA"):
            self.logger.info ("Using connected Pi camera module ...")
            #if (self._cam == None):
            #    self._cam = picamera.PiCamera()
            #    self._cam.start_preview()
        elif (self.cfg["uri"] != None):
            self.logger.info ("Using web camera at URI: %s ...",
                              self.cfg["uri"])
        else:
            self.logger.info ("Attempting to use local (USB?) camera ...")
            if ( self._cam == None):
                self._cam = Camera()

    def _takePiCameraPicture (self):
        self.logger.debug("started")
        self._cam = picamera.PiCamera()
        self._cam.start_preview()
        time.sleep(2)
        f = io.BytesIO()
        self._cam.capture(f, 'jpeg')
        self._cam.stop_preview()
        self.logger.debug("finished")
        return bytearray(f.getvalue())


    def _takeUSBCameraPicture (self):
        self.logger.debug("started")
        self._img = self._cam.getImage()

        self.logger.debug("captured image")
        f = io.BytesIO()
        self.logger.debug("XXX")
        self._img.getPIL().save(f,"JPEG")
        self.logger.debug("got byte array")
        return bytearray(f.getvalue())

    def _takeWebCameraPicture (self):
        """Take a picture from the HTTP enabled camera."""

        self.str = (urllib.urlopen(self.cfg["uri"])).read()
        self.logger.info("Picture taken on '%s'", self.cfg["uri"])

        return bytearray(self.str)

    def takePicture(self):
        try:
            if (self.cfg["uri"] == None):
                self.bytes = self._takeUSBCameraPicture()
            elif (self.cfg["uri"] == "PICAMERA"):
                self.bytes = self._takePiCameraPicture()
            else:
                self.bytes = self._takeWebCameraPicture()
        except:
            e = sys.exc_info()[0]
            self.logger.warning (
                "Failed to take picture - '%s' ... using '%s' instead.",
                str(e), self.cfg["no_pic"])
            self.str = open(self.cfg["no_pic"]).read()
            self.bytes = bytearray(self.str)
            #raise
            
        return self.bytes

                
    def getString (self):
        return self.str
    
    def getByteArray (self):
        """Return the picture that has been taken as an array of bytes."""

        return self.bytes

    def forwardSSHServer (self, strServer = 'localhost'):
        """Forward (copy) the picture that has been taken to the specified server using SSH."""

        cfg = self.cfg_root["ssh_destinations"][strServer]

        self.logger.info("started for %s", strServer)

        self.logger.info("Using file '%s' ...", self.cfg["local_path"])
        f = open(self.cfg["local_path"],'w')
        f.write(self.bytes)
        f.close()

        cfg.setdefault("path","/tmp/shot.jpg")
        cfg.setdefault("server", "localhost")
        cfg.setdefault("user", "root")
        cfg.setdefault("passwd", "123")
        self.logger.info (
            "Using %s@%s with path '%s' for ssh image copy destination.",
            cfg["user"], cfg["server"], cfg["path"])

        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(cfg["server"], username=cfg["user"],
                        password=cfg["passwd"], look_for_keys=False)
            sftp = ssh.open_sftp()
            sftp.put(self.cfg["local_path"], cfg["path"])
            sftp.close()
            ssh.close()
            self.logger.info ("Copied image '%s' to '%s:%s'",
                              self.cfg["local_path"], cfg["server"],
                              cfg["path"])
        except:
            e = sys.exc_info()[0]
            self.logger.error("Failed to copy picture: %s\n" % str(e))
            #raise

        return cfg["path"]

if __name__ == '__main__':

    # read config file and set logging level based on value in config file
    cfg = config.config()
    cfg.setLogging()

    obj = MyCamera (cfg, "pi")
    obj.takePicture()
    obj.forwardSSHServer("minecraft_server")

    #obj = MyCamera (cfg, "usb")
    #obj.takePicture()
    #obj.forwardSSHServer("minecraft_server")
