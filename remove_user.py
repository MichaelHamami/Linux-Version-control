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
    user_to_remove = sys.argv[2]
    filename = sys.argv[1]
    st = os.stat(filename)
    owner_name = pwd.getpwuid(st.st_uid).pw_name
    group_name = getgrgid(os.stat(filename).st_gid).gr_name
    user_run = os.getlogin()
    print(filename)
    print(owner_name)
    print(group_name)
    print(user_to_remove)
    print(user_run)
    root_password = "kosm1011"
    # todo - fix error of rm
    if user_run == owner_name:
        os.popen("echo {} | su -c 'gpasswd --delete {} {} > somefile.txt'".format(root_password, user_to_remove, group_name))

        # os.popen("rm somefile.txt")
    return 0


if __name__ == "__main__":
    main()
