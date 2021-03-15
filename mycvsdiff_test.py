#!/usr/bin/env python3


import glob
import sys
import os
import shutil
import subprocess
from decimal import *
from os import path

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
    #todo change first line - try ...
    # print(lines_for_temp[0])

    # lines_for_temp[0] = lines_for_temp[0].replace(".MYCVS/{}.copy".format(filename),"last_revision.txt",1)
    # print(lines_for_temp[0])
    # print(lines_for_temp)
    file_temp = open("temp_patchfile.patch","w")
    file_temp.writelines(lines_for_temp)
    file_temp.close()
    # create copy of .MYCVS/FILENAME.copy to save last revision.
    # shutil.copyfile(".MYCVS/{}.copy".format(filename),"last_revision.txt")
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
# file1 = original (input filename) file2 = last_revision patch = temp_patchfile.patch =(filename an)
def create_revision(file1, file2):
    print("create_revision called with file1: {} and file2: {}".format(file1,file2))
    file1 = open("temp_patchfile.patch","r")
    lines_for_last_revision = []
    for line in file1:
        if (line[0:3]!= "+++" and (line[0] == "+" or line[0] ==" ")):
            print("the line that added:{}".format(line))
            lines_for_last_revision.append(line[1:])
    
        # print("{} {}".format(line[0],line[1]))
    file1.close()
    file2 = open("revision.txt","w")
    file2.writelines(lines_for_last_revision)
    file2.close()
    return "revision.txt"
    # shutil.copyfile(".MYCVS/{}.copy".format(file1),"copy_first_before_patch.txt")
    # stream = os.popen('patch .MYCVS/{}.copy < {}'.format(file1,file2))
    # output = stream.readlines()
    # print(output)

    #using last revision
    # stream = os.popen('patch last_revision.txt {}'.format(file2))
    # return "last_revision.txt"

    #last use
    # Create an copy of the original file to temp copy
    # shutil.copyfile(".MYCVS/{}.copy".format(file1),"{}.copy".format(file1))
    # stream = os.popen('patch .MYCVS/{}.copy {}'.format(file1,file2))
    # stream = os.popen('cat .MYCVS/{}.copy'.format(file1))
    # output = stream.readlines()
    # print(output)

    # return ".MYCVS/{}.copy".format(file1)
def remove_temps():
    # stream = os.popen('cat .MYCVS/{}.copy'.format(file1))
    pass
def diff_revisions(file1,file2):
    print("diff_revisions called with file1: {} and file2: {}".format(file1,file2))

    stream = os.popen('diff -u {} {} > diff_current_work_and_last_revision.txt'.format(file1,file2))
    output = stream.readlines()
    print(output)
    # shutil.copyfile("{}.copy".format(file1),".MYCVS/{}.copy".format(file1))






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

    patch_file_revision = create_patch_file(revision,filename)
    patched_file = create_revision(filename,patch_file_revision)
    diff_revisions(filename,patched_file)
    # remove_temps()
    


if __name__ == "__main__":
    main()