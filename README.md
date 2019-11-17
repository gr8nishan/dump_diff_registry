# dump_diff_registry
This repository contains how to dump a registry and get difference between two registry dumps

## How to run diffing_registry.py

To use this file run below command in the windows command prompt

python diffing_registry.py

Once you run this it will ask for two file path of the registry dumps

Please enter path of registry dump 1 : <enter the path of file including file name,  in case the file is in current directory just give file name>

Please enter path of registry dump 2 : <enter the path of file including file name,  in case the file is in current directory just give file name>

It will print the total number of keys subkeys whose values are different or which has been created or deleted

In case of any error an error message will come and log will be created with name diffinglog.log in current directory

## How to run dumping_registry.py

To use this file run below command in the windows command prompt

python dumping_registry.py

Once you run this file it will create two files in the current directory named registry_dump_<timestamp>.pickle

There is a difference of 5 seconds in dumping the registry in both the files.

Once the dumping is successful it will print success message

In case of any error an error message will come and log will be created with name dumpinglog.log in current directory



