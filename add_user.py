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
    filename = sys.argv[1]
    st = os.stat(filename)
    ownername = pwd.getpwuid(st.st_uid).pw_name
    user_to_add = sys.argv[2]
    groupname = getgrgid(os.stat(filename).st_gid).gr_name
    username = os.getlogin()
    print(username)
    rootPassword = "kosm1011"
    if(username == ownername):
        os.popen("echo {} | su -c 'usermod -a -G {} {}'".format(rootPassword,groupname,user_to_add))
        # os.popen("echo {} | su -c 'deluser {} {}'".format(rootPassword,user_to_add,groupname))

    return 0

if __name__ == "__main__":
    main()