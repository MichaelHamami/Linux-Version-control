#!/usr/bin/env python3


import glob
import sys
import os
import shutil
import subprocess
from os import path
import pwd


def writerevision(filename):
    num_revision = getlastrevision(filename)
    current_revision = num_revision + 0.001
    file1 = open(".MYCVS/{}.myv".format(filename), "a")
    file1.write("\n#mycvs:{:.3f}\n".format(current_revision))
    stream = os.popen('diff -u .MYCVS/{}.copy {}'.format(filename,filename))
    output = stream.readlines()
    file1.writelines(output)
    file1.write("#endrevision:{:.3f}\n".format(current_revision))
    file1.close()

    
def getlastrevision(filename):
    stream = os.popen('tail -n 1 .MYCVS/{}.myv'.format(filename))
    output = stream.readlines()
    output = output[0].replace("\\n","")
    print(output)
    if "#endrevision" in output:
        num_revision = output[-6:]
        return float(num_revision)
    else:
        return 1.000

# TODO - need to check if the file is txt (only txt allowed)
def main():
    #  chack the user input is only 1 args 1 path is default and 1 file name
    if(len(sys.argv) != 2):
        print("please enter one file name")
        return 0
    print(sys.argv[1])
    filename = sys.argv[1]
    user_running = os.getlogin()
    st = os.stat(filename)
    ownername = pwd.getpwuid(st.st_uid).pw_name
    print("Current working directory: {0}".format(os.getcwd()))
    print("The directory .MYCVS exits? : {}".format(path.isdir(".MYCVS")))
    # check if there is a file with in our args ,
    if not path.exists(sys.argv[1]):
        print("There is no file exitsts with name: {}".format(sys.argv[1]))
        return 0

    if not path.isdir(".MYCVS"):
        print("first checkin !!")
        if(ownername != user_running):
            print("Only the owner of the file can do the first checkin")
            return 0

        rootPassword = "kosm1011"
        os.popen("echo {} | su -c 'groupadd group_{}'".format(rootPassword, filename))
        os.popen("echo {} | su -c 'chgrp group_{} {}'".format(rootPassword, filename,filename))

        # create .MYCVS Directory
        os.mkdir(".MYCVS")
        # Create an copy of the original file
        shutil.copyfile(sys.argv[1],".MYCVS/{}.copy".format(sys.argv[1]))
        file1 = open(".MYCVS/{}.myv".format(filename), "a")
        file1.write("start revesions")
        file1.close()
        return 0



    else:
        print("not first checkin")
        if(ownername != user_running):
            groupname = getgrgid(os.stat(filename).st_gid).gr_name
            stream = os.popen("members {} ".format(groupname))
            output = stream.readlines()
            print(output)
            if(user_running not in output):
                print("The user cant do checkin without been a group member of this file.")
                return 0
            
        
        writerevision(filename)
        return 0

if __name__ == "__main__":
    main()