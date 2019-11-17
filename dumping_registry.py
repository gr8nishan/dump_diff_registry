"""
To use this file run below command in the windows command prompt

python dumping_registry.py

Once you run this file it will create two files in the current directory named registry_dump_<timestamp>.pickle

There is a difference of 5 seconds in dumping the registry in both the files

In case of any error an error message will come and log will be created with name dumpinglog.log in current directory

"""
from winreg import *
import pickle
import threading
import time
import logging

logging.basicConfig(filename="dumpinglog.log",level=logging.ERROR)

class DumpRegistry:
    """
    This class has functions that can be used to dump registry in a pickle file
    """
    def __init__(self,file_name):
        """
        Constructor of the class
        """
        self.__file_name = file_name
        self.__hives = {"HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
                        "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
                        "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
                        "HKEY_USERS": HKEY_USERS,
                        "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
                        "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG}

    def read_key(self, key, path):
        """
        :param key: This is the key which is traversed and all values are read.
                    Should be a handle from OpenKey or HKEY_* constants.
        :param path: The path of te key in directory format
        :return: list of all the values of keys and sub keys within the key
        """
        stack_key = []
        stack_path = []
        final_dict = dict()
        stack_key.append(key)
        stack_path.append(path)
        while len(stack_key) > 0:
            try:
                key = stack_key.pop()
                path = stack_path.pop()
                no_sub_key, no_value, _ = QueryInfoKey(key)
                if no_sub_key > 0:
                    if no_value > 0:
                        for l in range(0, no_value):
                            name, value, _ = EnumValue(key, l)
                            final_dict[path+"\\"+name] = value
                    for i in range(0, no_sub_key):
                        sub_key = EnumKey(key, i)
                        stack_key.append(OpenKey(key, sub_key))
                        stack_path.append(path + "\\" + sub_key)
                else:
                    for l in range(0, no_value):
                        name, value, _ = EnumValue(key, l)
                        final_dict[path+"\\"+name] = value
            except OSError as e:
                logging.error("OSError occurred " + str(e))
                continue
            except EnvironmentError as e:
                logging.error("EnvironmentError occurred " + str(e))
                continue
            except WindowsError as e:
                logging.error("WindowsError occurred " + str(e))
                continue
            except Exception as e:
                logging.error("BaseException occurred " + str(e))
                continue
        return final_dict

    def read_hives(self):
        """
        This function will traverse through all the Hkey_constant* and append the keys and
         sub keys in a list of dictionary
        :return: list of dictionary
        """
        registry_dump = dict()
        for key in self.__hives.keys():
            hive_dump = self.read_key( self.__hives[key],key)
            registry_dump.update(hive_dump)
        return registry_dump

    def dump_registry(self):
        """
        This function will dump the registry into a json file
        """
        with open(self.__file_name, 'wb') as fout:
            pickle.dump(self.read_hives(), fout)


if __name__ == "__main__":
    """
    This function will dump the registry in pickle file
    When the file is executed it start a thread to dump first registry
    Then time.sleep command is given for 5 seconds before second thread gets executed
    Once both the files are saved a success message appears on the screen
    In case of any error an exception message will appear
    """
    try :
        registry1 = DumpRegistry("registry_dump_" + time.strftime("%Y%m%d-%H%M%S") + ".pickle")
        t1 = threading.Thread(target=registry1.dump_registry)
        # starting thread 1
        t1.start()

        #sleep for 5 seconds
        time.sleep(5)

        registry2 = DumpRegistry("registry_dump_" + time.strftime("%Y%m%d-%H%M%S") + ".pickle")
        t2 = threading.Thread(target=registry2.dump_registry)
        # starting thread 2
        t2.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
        # both threads completely executed

        print("Registry dumps have been taken successfully")
    except Exception as e:
        logging.error("Exception occurred" + str(e))
        print("An error has occurred. Please check the log file dumpinglog.log to know more details")