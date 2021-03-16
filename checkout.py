#!/usr/bin/env python3

import glob
import sys
import os
import shutil
import subprocess
from decimal import *
from os import path


def create_revision():
    file1 = open("temp_patchfile.patch","r")
    lines_for_last_revision = []
    for line in file1:
        if (line[0:3]!= "+++" and (line[0] == "+" or line[0] ==" ")):
            # print("the line that added:{}".format(line))
            lines_for_last_revision.append(line[1:])
    
    file1.close()
    file2 = open("revision.txt","w")
    file2.writelines(lines_for_last_revision)
    file2.close()
    return "revision.txt"

def create_patch_file(revision,filename):
    print("create_patch_file called with revision: {} and filename: {}".format(revision,filename))
    file1 = open(".MYCVS/{}.myv".format(filename))
    start_revision = False
    lines_for_temp = []
    for line in file1:
        if "#endrevision:{}".format(revision) in line:
            break  
        if start_revision:
            lines_for_temp.append(line)
        else:
            if "#mycvs:{}".format(revision) in line:
                start_revision = True
    file1.close()
    file_temp = open("temp_patchfile.patch","w")
    file_temp.writelines(lines_for_temp)
    file_temp.close()
    return "temp_patchfile.patch"

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
def main():
    print(sys.argv)
    #  chack the user input is only 1 args 1 path is default and 1 file name
    if(len(sys.argv) != 4 and len(sys.argv) != 2):
        print("please enter one file name or -r then revision and then one filename")
        return 0
    if(len(sys.argv) == 4):
        filename = sys.argv[3]
        revision = sys.argv[2]
        print(revision)
    else:
        filename = sys.argv[1]
        revision = getlastrevision(filename)
    if(ownername != user_running):
        groupname = getgrgid(os.stat(filename).st_gid).gr_name
        stream = os.popen("members {} ".format(groupname))
        output = stream.readlines()
        print(output)
        if(user_running not in output):
            print("The user cant do checkin without been a group member of this file.")
            return 0
        
    create_patch_file(revision,filename)
    create_revision()
    f = open("revision.txt", "r")
    print(f.read())
    f.close()
    return 0





    


if __name__ == "__main__":
    main()