"""Module for dealing with program configuration data.
   Config data can come from two places:
   - The command line
   - a YAML configuration file

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
from NestedDict import NestedDict

class config(NestedDict):
    """Class to deal with program configuration settings

       Configuration setting are taken from two locations:
       - the command line
       - a YAML configuration file

       By default the config file used is ./config.yml.
       The default can be overridden on the command line using -f.
       """

    def __init__(self, *args):
        """create an instance of this class
        """
        NestedDict.__init__(self)
        
        logging.basicConfig(
            format='%(levelname) -10s %(asctime)s %(module)s:%(funcName)s[%(lineno)s] %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)

        parser = argparse.ArgumentParser ()
        parser.add_argument('-f', action='store', dest='file',
                            default='./config.yml',
                            help='Load config file ... ./config.yml used by default')
        results = parser.parse_args()

        f = open(results.file)
        data = yaml.safe_load(f)     # use safe_load instead of load
        f.close()

        logging.info ("Using config file %s", results.file)

        # copy dict values from YAML file over to nested dictionary
        self.copy_recursive(data, self)


    def dump (self):
        """Return the config data as a readable string."""

        return yaml.dump(self)

    def setLogging (self):
        """Set final logging level based on contents of config file"""

        logging.basicConfig(
            format='%(levelname) -10s %(asctime)s %(module)s:%(funcName)s[%(lineno)s] %(message)s')

        logging.getLogger().setLevel(getattr(logging, self.get("logging.root.level", "INFO").upper()))

        self.logger.debug("Config File contents => %s", self.dump())

if __name__ == '__main__':

    logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(funcName)s[%(lineno)s] %(message)s',
                            level="DEBUG")

    cfg = config()
    cfg.setLogging()
    
    logging.info("Config file contents: %s", cfg.dump())

    cfg["XXX"] = "test1"
    cfg["YYY.test2"] = "a"
    cfg["QQQ.test3.a"] = "b"
    cfg["RRR.test3"] = "b"
    cfg["RRR.test4.a"] = "c"

    logging.info("Config file contents: %s", cfg.dump())
