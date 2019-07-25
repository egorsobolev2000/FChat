#!/usr/bin/python3
# -*- coding: utf-8 -*-clear
import sys
import os


def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))

if sys.version_info<(3,5,0):
  sys.stderr.write("\033[91mYou need python 3.5 or later to run this script\033[00m\n")
  exit(1)
else:
    print("\x1b[6;37;41m Attention! \x1b[0m", "\x1b[6;37;44m Python interpreter version should be no lower than 3.5 \x1b[0m")

    prYellow("Install PyAutoGUI ...")
    os.system("pip install pyautogui")
    prYellow("Install virtualenv ...")
    os.system("pip install virtualenv")
    prYellow("Install termcolor ...")
    os.system("pip install termcolor")
    prYellow("Install pusher ...")
    os.system("pip install pusher git+https://github.com/nlsdfnbch/Pysher.git python-dotenv")
    os.system("chmod +x terminalChat.py")
    os.system("ls")
    print("Let's start, print >>> \033[92mpython ./terminalChat.py\033[00m")
    exit(1)
