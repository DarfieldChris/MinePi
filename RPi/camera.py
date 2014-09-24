"""Module for capturing an image (a picture) from a web-based camera"""

#Standard Library Imports
import logging
import sys
import os
import subprocess

# Third Party Imports
import urllib
import paramiko

# Local Application/Library Specific Imports
import config

class Camera:
    """Class to download images from an http enabled or USB camera
    (so could actually be any web server)"""

    def __init__(self, cfg, strCamera = "basic"):
        """Create an instance of this class.

           Arguments:
               strCamera - The key identifying the camera to use, 
                           this camera must be defined in the config file.
                           This key will be resolved to 'cameras.' + strCamera (e.g. cameras.dads_camera)
        """

        self.cfg = cfg
        self.strCameraURI = cfg.get("cameras",strCamera,"uri", default=None)
        self.strCameraCmd = cfg.get("cameras",strCamera,"cmd", default=None)
        self.strLocalPath = "./images/shot.jpg"
        self.strNoPic = cfg.get("cameras",strCamera,"no_pic_available","./images/xxx.jpg")
        if (self.strCameraURI != None):
            logging.info ("Using web camera at URI: %s", self.strCameraURI)
        else:
            logging.info ("Using local (USB?) camera: %s", self.strCameraCmd)


    def _takeUSBCameraPicture (self):
        #logging.info("1Picture taken with '%s'", self.strCameraCmd)
        sp = subprocess.Popen(self.strCameraCmd.split(' '), stdout=subprocess.PIPE)
        #sp = subprocess.Popen(["/usr/bin/fswebcam","-"], stdout=subprocess.PIPE)
        #logging.info("2Picture taken with '%s'", self.strCameraCmd)
        self.str = sp.stdout.read()
        logging.info("Picture taken with '%s'", self.strCameraCmd)
        return bytearray(self.str)

    def _takeWebCameraPicture (self):
        """Take a picture from the HTTP enabled camera."""

        self.str = (urllib.urlopen(self.strCameraURI)).read()
        logging.info("Picture taken on '%s'", self.strCameraURI)
            
        #self.strPic, headers = urllib.urlretrieve(self.strCameraURI,self.strLocalPath)
        #logging.info("Picture taken on '%s' as '%s'", self.strCameraURI, self.strPic)

        return bytearray(self.str)

    def takePicture(self):
        try:
            if (self.strCameraURI == None):
                self.bytes = self._takeUSBCameraPicture()
            else:
                self.bytes = self._takeWebCameraPicture()
        except:
            e = sys.exc_info()[0]
            logging.warning ("Failed to take picture - '%s' ... using '%s' instead.", str(e), self.strNoPic)
            self.str = open(self.strNoPic).read()
            self.bytes = bytearray(self.str)
            #raise
            
        return self.bytes

                
    def getString (self):
        return self.str
    
    def getByteArray (self):
        """Return the picture that has been taken as an array of bytes."""

        #f = open(self.strPic)
        #imagestring = f.read()
        #byteArray = bytes(imagestring)
        return self.bytes

    def forwardSSHServer (self, strServer = 'localhost'):
        """Forward (copy) the picture that has been taken to the specified server using SSH."""

        logging.info("forwardSSHServer: started for %s", strServer)

        logging.info("forwardSSHServer: Using file '%s' ...", self.strLocalPath)
        f = open(self.strLocalPath,'w')
        f.write(self.str)
        f.close()

        strRemotePath = self.cfg.get("ssh_destinations", strServer, "path","/tmp/shot.jpg")
        strMinecraftURI = self.cfg.get("ssh_destinations", strServer, "server", "localhost")
        strMinecraftUser = self.cfg.get("ssh_destinations", strServer, "user", "root")
        strMinecraftPasswd = self.cfg.get("ssh_destinations", strServer, "passwd", "123")
        logging.info ("Using %s@%s with path '%s' for ssh image copy destination.", strMinecraftUser, strMinecraftURI, strRemotePath)

        self.strRemotePath = strRemotePath

        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            #logging.info("forwardMinecraft: 1");
            ssh.connect(strMinecraftURI, username=strMinecraftUser, password=strMinecraftPasswd, look_for_keys=False)
            #logging.info("forwardMinecraft: 2");
            sftp = ssh.open_sftp()
            #logging.info("forwardMinecraft: 3");
            sftp.put(self.strLocalPath, strRemotePath)
            #logging.info("forwardMinecraft: 4");
            sftp.close()
            ssh.close()
            logging.info ("Copied image '%s' to '%s:%s'", self.strLocalPath, strMinecraftURI, strRemotePath)
        except:
            e = sys.exc_info()[0]
            logging.error("Failed to copy picture: %s\n" % str(e))
            #raise

if __name__ == '__main__':

    # set default logging level prior to parsing config info
    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

    # read config file and set logging level based on value in config file
    cfg = config.YAMLConfig()
    cfg.setLogging()

    #obj = Camera (cfg, "dad_phone")
    #obj.takePicture()
    #obj.forwardSSHServer("minecraft_server")

    obj = Camera (cfg, "usb")
    obj.takePicture()
    obj.forwardSSHServer("minecraft_server")
