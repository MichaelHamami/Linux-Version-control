#!/usr/bin/env python3


import glob
import sys
import os
import shutil
import subprocess
from decimal import *
from os import path
import pwd
from grp import getgrgid

def main():
    #  chack the user input is only 1 args 1 path is default and 1 file name
    if(len(sys.argv) != 3):
        print("please enter file name and then username")
        return 0
    user_to_remove = sys.argv[2]
    filename = sys.argv[1]
    st = os.stat(filename)
    ownername = pwd.getpwuid(st.st_uid).pw_name
    groupname = getgrgid(os.stat(filename).st_gid).gr_name
    user_run = os.getlogin()
    print(filename)
    print(ownername)
    print(groupname)
    print(user_to_remove)
    print(user_run)
    rootPassword = "kosm1011"
    # todo - fix error of rm
    if(user_run == ownername):
        os.popen("echo {} | su -c 'gpasswd --delete {} {} > somefile.txt'".format(rootPassword,user_to_remove,groupname))

        # os.popen("rm somefile.txt")
    return 0

if __name__ == "__main__":
    main()