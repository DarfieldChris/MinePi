# Standard Library Imports
import logging

# Third Party Imports

# Local/Application Specific Imports


class NestedDict(dict):

    __SPLIT = '.'
    
    def __init__(self, *args):
        dict.__init__(self, args)

        self.logger = logging.getLogger(self.__class__.__name__)

    def __IsInt(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    def __get_nested_dict(self, key):
        index = str(key).split(self.__SPLIT, 1)
        if (self.__IsInt(index[0])):
            key1 = int(index[0])
        else:
            key1 = index[0]

        if ( key1 not in self ):
                self[key1] = NestedDict()

        if (len(index) > 1):
            ret = (self[key1]).__get_nested_dict(index[1])
        else:
            ret = self[key1] 

        return ret
    
    def __getitem__(self, key):
        index = str(key).rsplit(self.__SPLIT, 1)

        if (len(index) > 1):
            # nested key of the form 'a.b.c' ... find the nested dict!!!
            nested_dict = self.__get_nested_dict(index[0])
            if (self.__IsInt(index[1])):
                key1 = int(index[1])
            else:
                key1 = index[1]
            val = dict.__getitem__(nested_dict, key1)
        else:         
            # this is a standard key of the form 'a' ... just behave normally
            val = dict.__getitem__(self,key)
        
        self.logger.debug("'%s' = %s", str(key), str(val))
        return val

    def __setitem__(self, key, val):
        index = str(key).rsplit(self.__SPLIT, 1)

        if (len(index) > 1):
            # nested key of the form 'a.b.c' ... find the nested dict!!!
            nested_dict = self.__get_nested_dict(index[0])
            if (self.__IsInt(index[1])):
                key1 = int(index[1])
            else:
                key1 = index[1]
            dict.__setitem__(nested_dict, key1, val)
        else:         
            # this is a standard key of the form 'a' ... just behave normally
            dict.__setitem__(self, key, val)
            
        self.logger.debug("'%s' = %s", str(key), str(val))

    def get (self, key, default=None):
        index = str(key).rsplit(self.__SPLIT, 1)

        if (len(index) > 1):
            # nested key of the form 'a.b.c' ... find the nested dict!!!
            nested_dict = self.__get_nested_dict(index[0])
            if (self.__IsInt(index[1])):
                key1 = int(index[1])
            else:
                key1 = index[1]
            val = dict.get(nested_dict, key1, default)
        else:
            val = dict.get(self,key,default)

        self.logger.debug("'%s' = %s", str(key), str(val))

        return val

    def setdefault (self, key, default=None):
        index = str(key).rsplit(self.__SPLIT, 1)

        if (len(index) > 1):
            # nested key of the form 'a.b.c' ... find the nested dict!!!
            nested_dict = self.__get_nested_dict(index[0])
            if (self.__IsInt(index[1])):
                key1 = int(index[1])
            else:
                key1 = index[1]
            val = dict.setdefault(nested_dict, key1, default)
        else:
            val = dict.setdefault(self,key,default)

        self.logger.debug("'%s' = %s", str(key), str(val))

        return val

    def copy_recursive(self, orig_dict, new_dict):
        for key in orig_dict:
            if isinstance(orig_dict[key],dict):
                new_dict[key] = NestedDict()
                self.copy_recursive(orig_dict[key], new_dict[key])
            else:
                new_dict[key] = orig_dict[key]

    def getBoolean(self, key, default = False):
        s = self.get(key)

        if s is True or s is False:
            return s

        s = str(s).strip().lower()

        res = not s in ['false','f','n','0','']

        self.logger.debug("Boolean value is: %d", res)

        return res


        
if __name__ == '__main__':

    logging.basicConfig(format='%(levelname) -10s %(asctime)s %(module)s:%(funcName)s[%(lineno)s] %(message)s',
                            level="DEBUG")

    a = NestedDict()

    a['x'] = 'b'
    a['y.1'] = 'q'
    a['y.2.3'] = 'b'

    
