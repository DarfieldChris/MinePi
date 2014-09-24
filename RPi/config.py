"""Module for reading/writing the contents of a configuration file

This module provides a consistent means of accessing/saving configuration settings.

Only YAML files are currently supported.
Only reading config values is currently supported.
"""

#Notes:
#    1 - Comments and code style follows "Style Guide For Python Code"

# Standard Library Imports
import argparse
import logging

# Third Party Imports
import yaml

#Local Application/Library Specific Imports
# --- DO NOT HAVE ANY ---

class YAMLConfig:
    """Class to deal with YAML configuration files"""

    def __init__(self):
        """create an instance of this class

              By default the config file used is ./config.yml.
              The default can be overridden on the command line using -f.
        """

        parser = argparse.ArgumentParser ()
        parser.add_argument('-f', action='store', dest='file',
                        default='./config.yml',
                        help='Load config file ... ./config.yml used by default',
                        )
        results = parser.parse_args()

        f = open(results.file)
        self.data = yaml.safe_load(f)     # use safe_load instead of load
        f.close()
        logging.info ("Using config file %s", file)
 
    def getBoolean(self, list, obj = None, key = None, default = False):
        s = self.get(list,obj,key,default)

        if s is True or s is False:
            return s

        s = str(s).strip().lower()

        res = not s in ['false','f','n','0','']

        logging.debug("Boolean value is: %d", res)

        return res

    def get(self, list, obj = None, key = None, default = "default"):
        """Get the value for the specified key and return it as a string.

           The key can take one of three forms:
               list.obj.key = ???
               list.obj = ???
               list = ???

           Parameters:
               list (String)    - first part of the key (eg 'a' in a.b.c)
               obj  (String)    - second part of key ... if not specified key is only 'list'
               key  (String)    - third part of key ... if not specified key is only 'list.oj'
               default (String) - default value to return if specified key does not exist
        """

        val = default

        try:
            if obj == None:
                val = self.data[list]
                logging.debug("get: %s = %s",list,val)
            elif key == None:
                val = self.data[list][obj]
                logging.debug("get: %s.%s = %s",list,obj,val)
            else:
                val = self.data[list][obj][key]
                logging.debug("get: %s.%s.%s = %s",list,obj,key,val)
        except:
            logging.warning ("get: - Failed to get %s.%s.%s ... using default value '%s'",
                              list, obj, key, default)
            val = default

        return val

    def dump (self):
        """Return the config file data as a readable string."""

        return yaml.dump(self.data)

    def setLogging (self):
        """Set final logging level based on contents of config file"""

        logging.getLogger().setLevel(getattr(logging, self.get("log_level", default = "DEBUG")))
        logging.debug("Config File contents => %s", self.dump())

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

    cfg = YAMLConfig()

    logging.info("Config file contents: %s", cfg.dump())
