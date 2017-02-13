#!/usr/bin/env python
from public import *

run("cat /proc/interrupts", 10)

subprocess.Popen("feh ../lab1b/out1.pgm", shell=True)
