import sys
import os
import argparse
import glob
import subprocess
import shlex
import random
import time
import csv
import re
from threading import Timer

def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [
        proc])

    try:
        timer.start()
        (stdout, stderr) = proc.communicate()
    finally:
        output = stdout[-20000:]
        print output
        print stderr
        timer.cancel()

def stringToTimeList(timestring):
    timestring = timestring.upper()
    if len(timestring) != 14:
        print 'Incorrect deadline format.'
        raise SystemExit
    timelist = []
    timelist.append(timestring[0:4])
    timelist.append(timestring[4:6])
    timelist.append(timestring[6:8])
    timelist.append(timestring[8:10])
    timelist.append(timestring[10:12])
    timelist.append(timestring[12:])
    return timelist


def EEETimeToTimeList(EEETime):
    EEETime = EEETime.upper()
    ll = EEETime.split(' ')
    timelist = []
    timelist.append(ll[0][0:4])
    timelist.append(ll[0][5:7])
    timelist.append(ll[0][8:10])
    tl = ll[1].split(':')
    timelist.append(tl[0])
    timelist.append(tl[1][0:2])
    timelist.append(tl[1][2:])
    return timelist


def laterThan(sub_time_list, ddl_time_list):
    if int(sub_time_list[0]) < int(ddl_time_list[0]):
        return False
    if int(sub_time_list[0]) > int(ddl_time_list[0]):
        return True
    if int(sub_time_list[1]) < int(ddl_time_list[1]):
        return False
    if int(sub_time_list[1]) > int(ddl_time_list[1]):
        return True
    if int(sub_time_list[2]) < int(ddl_time_list[2]):
        return False
    if int(sub_time_list[2]) > int(ddl_time_list[2]):
        return True
    if sub_time_list[-1] != ddl_time_list[-1]:
        if sub_time_list[-1] == 'AM' and ddl_time_list[-1] == 'PM':
            return False
        if sub_time_list[-1] == 'PM' and ddl_time_list[-1] == 'AM':
            return True
    if int(sub_time_list[3]) < int(ddl_time_list[3]):
        return False
    if int(sub_time_list[3]) > int(ddl_time_list[3]):
        return True
    if int(sub_time_list[4]) <= int(ddl_time_list[4]):
        return False
    return True

