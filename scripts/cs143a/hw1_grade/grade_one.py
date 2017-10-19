#!/usr/bin/env python
import sys
import os
import argparse
import glob
import shlex
import random
import time
import csv
import re
from subprocess import Popen, PIPE
from threading import Timer

parser = argparse.ArgumentParser(description='Inputs.')
parser.add_argument('-i', '--index', type=str,
        help='student index in the gradebook')
parser.add_argument('-f', '--files', type=str, nargs='*',
        help='submitted files')

args = parser.parse_args()

def run_with_stdin(cmd, std_in, timeout_sec):
    proc = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE)

    kill_proc = lambda p: p.kill()
    timer = Timer(timeout_sec, kill_proc, [
        proc])

    output = ''
    try:
        timer.start()
        (stdout, stderr) = proc.communicate(input=std_in)
    finally:
        output = stdout[-1000:]
        timer.cancel()
    return output

total_score = 100
extra_total_score = 21
extra_implemented = False
submission_dir = '../../submissions/'
gradebook = '../../group_grades.csv'

if not os.path.exists(gradebook):
    raise SystemExit('Gradebook not found.')

idx = args.index
files = args.files

comments = ''
srcs = []
extra_srcs = []
for f in files:
    if f.endswith('.c'):
        if "extra" in f:
            extra_srcs.append(f)
        else:
            srcs.append(f)
    if f.endswith('.zip'):
        comments += 'Zip file uploaded; '

print
score = 0
if len(srcs) == 0:
    comments += 'No source file submitted; '
    print 'No source file submitted.'
else:
    if len(srcs) > 1:
        print 'Warning: multiple source files submitted.'
    for src in srcs:
        binary = './out'
        compile_cmd = 'gcc -o ' + binary + ' ' + submission_dir + src

        run_with_stdin(compile_cmd, '', 3)
        if not os.path.exists(binary):
            comments += 'Compiling ' + src + ' failed; '
            continue
        else:
            score += 5
            print 'Compilation...Passed.'

        # Score distribution:
        # - Compilation(5)
        # - Exec(20): test1(20)
        # - Redir(30): test2_1(15), test2_2(15)
        # - Pipe(35): test3_1(20), test3_2(15)
        # - Combination(10): test4(10)

        # --------------Exec----------------
        cmd_in = ''
        with open ('test1.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 1..',
        output = run_with_stdin(binary, cmd_in, 3)
        if 'Test 1 passed.' in output:
            score += 20
            print 'Passed.'
        else:
            comments += 'Test1 failed; '
            print 'Failed.'

        # --------------Redir---------------
        cmd_in = ''
        with open ('test2_1.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 2_1..',
        output = run_with_stdin(binary, cmd_in, 3)
        if output.strip() == '8':
            score += 15
            print 'Passed.'
        else:
            comments += 'Test2_1 failed; '
            print 'Failed.'

        cmd_in = ''
        with open ('test2_2.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 2_2..',
        output = run_with_stdin(binary, cmd_in, 3)
        if os.path.exists('./test2.txt'):
            f = open('test2.txt', 'r')
            res = f.read()
            if 'Test 2_2 passed.' in res:
                score += 15
                print 'Passed.'
            else:
                comments += 'Test2_2 failed; '
                print 'Failed.'
        else:
            comments += 'Test2_2 failed; '
            print 'Failed.'

        # --------------Pipe---------------
        cmd_in = ''
        with open ('test3_1.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 3_1..',
        output = run_with_stdin(binary, cmd_in, 3)
        if output.strip() == '15':
            score += 20
            print 'Passed.'
        else:
            comments += 'Test3_1 failed; '
            print 'Failed.'

        cmd_in = ''
        with open ('test3_2.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 3_2..',
        output = run_with_stdin(binary, cmd_in, 3)
        if output.strip() == '12':
            score += 15
            print 'Passed.'
        else:
            comments += 'Test3_2 failed; '
            print 'Failed.'

        # -------------Comb---------------
        cmd_in = ''
        with open ('test4.sh', 'r') as f:
            cmd_in = f.read()
        print 'Running test 4..',
        output = run_with_stdin(binary, cmd_in, 3)
        if os.path.exists('./test4.txt'):
            f = open('test4.txt', 'r')
            res = f.read()
            if res.strip() == '12':
                score += 10
                print 'Passed.'
            else:
                comments += 'Test4 failed; '
                print 'Failed.'
        else:
            comments += 'Test4 failed; '
            print 'Failed.'

print

extra_score = 0
if len(extra_srcs) == 0:
    extra_implemented = False
    print 'Extra credits not implemented.'
else:
    extra_implemented = True
    print 'Extra credits implemented.'
#    if len(extra_srcs) > 1:
#        print 'Warning: multiple extra credit source files submitted.'
#    for src in extra_srcs:
#        binary = './extra_out'
#        compile_cmd = 'gcc -o ' + binary + ' ' + submission_dir + src
#
#        run(compile_cmd, 3)
#        if not os.path.exists(binary):
#            comments += 'Compiling ' + src + ' failed; '
#            continue
#
#        # --------------CmdList--------------
#        cmd_in = ''
#        with open ('test1.sh', 'r') as f:
#            cmd_in = f.read()
#        print 'Running test 1..',
#        output = run_with_stdin(binary, cmd_in, 3)
#        if 'Test 1 passed.' in output:
#            score += 20
#            print 'Passed.'
#        else:
#            comments += 'Test1 failed; '
#            print 'Failed.'
#
#        # ------------SubShell--------------
#
#        # ------------Background------------

if score > total_score or extra_score > extra_total_score:
    comments = 'INVALID SCORE please check!!!' + comments

print 'Score: ' + str(score)
print 'Comments: ' + comments

# line format: index,score,extra,comments,files
comments = comments.strip().strip(';')
line = ",".join([idx, str(score), str(extra_implemented), comments, "; ".join(files)])
with open(gradebook, 'a+') as f:
    f.write(line + '\n')

