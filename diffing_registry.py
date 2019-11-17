"""
To use this file run below command in the windows command prompt

python diffing_registry.py

Once you run this it will ask for two file path of the registry dumps

Please enter path of registry dump 1 : <enter the path of file including file name,
                                        in case the file is in current directory just give file name>

Please enter path of registry dump 2 : <enter the path of file including file name,
                                        in case the file is in current directory just give file name>

In case of any error an error message will come and log will be created with name diffinglog.log in current directory

"""

import pickle
from os import path
import logging
import threading
import queue

logging.basicConfig(filename="diffinglog.log",level=logging.ERROR)

class DiffingRegistry:
    """
    This class will compare two registry dumps and list all keys subkeys whose value has been changed or
    any key subkey has been added or deleted
    """
    def __init__(self):
        """
        constructor of the class
        """
    def read_dump(self,filepath):
        """
        This function will read a registry dump into a dictionary
        :return: list of dictionary
        """
        with open(filepath,'rb') as f:
            dump = pickle.load(f)
        return dump

    def compare_dict(self,dict1,dict2):
        """
        This function will compare two registry dictionaries
        :param dict1: dictionary 1
        :param dict2: dictionary 2
        :return: list of keys that are different
        """
        difference = []
        for key in dict1:
            if key in dict2:
                if dict1[key] != dict2[key]:
                    difference.append(key)
            else:
                difference.append(key)
        return difference


if __name__ == "__main__":
    """
    This function will take two file path as input from user.
    Then it will load both the files.
    Then we will identify the difference between both the files using threads and display the results
    """
    try:
        filepath1 = str(input("Please enter path of registry dump 1 : "))
        filepath2 = str(input("Please enter path of registry dump 2 : "))

        if path.exists(filepath1) and path.exists(filepath2):
            diffing_registry = DiffingRegistry()
            dump1 = diffing_registry.read_dump(filepath1)
            dump2 = diffing_registry.read_dump(filepath2)

            que = queue.Queue()
            que1 = queue.Queue()
            t = threading.Thread(target=lambda q, arg1, arg2:
                                q.put(diffing_registry.compare_dict(arg1,arg2)), args=(que, dump1, dump2))

            t1 = threading.Thread(target=lambda q1, arg1, arg2:
                                q1.put(diffing_registry.compare_dict(arg1, arg2)), args=(que1, dump2, dump1))

            t.start()
            t1.start()
            t.join()
            t1.join()

            final_result = list(set(que.get()+que1.get()))
            print("Total number of keys that have been modified added or deleted ", len(final_result))
            [print(result) for result in final_result]
        else:
            print("One of the file does not exist. Please restart the program and enter correct file path!!")
    except Exception as e:
        logging.error("Exception occurred" + str(e))
        print("An error has occurred. Please check the log file diffinglog.log to know more details!!")