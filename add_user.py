#!/usr/bin/env python3


import sys
import os
import pwd
from grp import getgrgid


def main():
    #  chack the user input is only 1 args 1 path is default and 1 file name
    if len(sys.argv) != 3:
        print("please enter file name and then username")
        return 0
    filename = sys.argv[1]
    st = os.stat(filename)
    owner_name = pwd.getpwuid(st.st_uid).pw_name
    user_to_add = sys.argv[2]
    group_name = getgrgid(os.stat(filename).st_gid).gr_name
    user_name = os.getlogin()
    print(user_name)
    root_password = "kosm1011"
    if user_name == owner_name:
        os.popen("echo {} | su -c 'usermod -a -G {} {}'".format(root_password, group_name, user_to_add))

    return 0


if __name__ == "__main__":
    main()
