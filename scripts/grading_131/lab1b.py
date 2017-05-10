#!/usr/bin/env python
from public import *

parser = argparse.ArgumentParser(description='Inputs to grade lab assignments.')
parser.add_argument('-d', '--directory', type=str,
        help='The directory to the assignment')
parser.add_argument('-t', '--deadline', type=str,
        help='Deadline of the assignment, in the format of YYYYMMDDHHMMAM or YYYYMMDDHHMMPM')
parser.add_argument('-l', '--lang', type=str,
        help='Type of language: c or c++ (lower case)')
parser.add_argument('-s', '--score', type=int,
        help='Full score')

args = parser.parse_args()

print "Now grading "+args.directory+", deadline is set at " + args.deadline + "!"

full_score = args.score
prefix = args.directory
if args.directory[-1] != "/":
    prefix += "/"

for f in glob.glob(prefix+"*.csv"):
        csv_in = f

if args.lang == "c++":
    suffix = ".cpp"
    CC = "g++"
elif args.lang == "c":
    suffix = ".c"
    CC = "gcc"
else:
    print "Unsupported language."
    raise SystemExit

num_lines = 0
pgm_out = prefix+"out1.pgm"
csv_out = prefix+"grades.csv"

comp_binary = prefix+"binary"
cmd_comp_no_src = CC+" -std=c++11 -pthread -o "+comp_binary+" "
cmd_run = comp_binary+" "+prefix+"aniketsh_tc1.pgm "+prefix+"out1.pgm 4 32"
cmd_open = "feh "+pgm_out

if os.path.exists(csv_out):
    cancelled = raw_input("Do you want to delete the grades? Press enter (delete) or any other key (not delete):")
    if not cancelled:
        os.remove(csv_out)
    else:
        num_lines = sum(1 for line in open(csv_out))

count = 0

writer = csv.writer(open(csv_out, 'a'))


with open(csv_in, 'rb') as csvfile:
    submissions = csv.reader(csvfile)
    for record in submissions:
        count += 1
        if (count <= num_lines):
            continue
        if os.path.exists(comp_binary):
            os.remove(comp_binary)
        if os.path.exists(pgm_out):
            os.remove(pgm_out)

        # Grading rubrics
        grades = full_score
        grade_comments = ""

        # Source file
        comp_src = ""
        comp_timelist = []

        files = [ i.strip() for i in record[3].split(";")]
        for f in files:
            ll = [ i.strip() for i in f.split("(")]
            file_name = ll[0]
            eee_time = ll[1][9:-1]
            if file_name.endswith(suffix):
                comp_src = prefix+"Files/"+file_name
                comp_timelist = EEETimeToTimeList(eee_time)

        if not comp_src:
            grades = 0
            grade_comments += "No source file found; "
            record[2] = str(grades)
            record.append(grade_comments)
            print "No source file found for " + record[1] + ", skipping..."
            writer.writerow(record)
            continue

        if laterThan(comp_timelist, stringToTimeList(args.deadline)):
            grades -= 20
            grade_comments += "overdue (-20); "

        # Try to compile the file
        run(cmd_comp_no_src+comp_src, 10)

        # Check if binary got compiled
        if not os.path.exists(comp_binary):
            grades = 5
            grade_comments += "compilation failed; "
            record[2] = str(grades)
            record.append(grade_comments)
            writer.writerow(record)
            continue

        # Execute the binary
        run(cmd_run, 30)

        # Check if output image exist
        if not os.path.exists(pgm_out):
            grades = 10
            grade_comments += "no output image generated; "
            record[2] = str(grades)
            record.append(grade_comments)
            writer.writerow(record)
            continue

        # Open output image file
        subprocess.Popen(cmd_open, shell=True)

        failure_code = raw_input("Please check the results, now choose pass (enter), minor error (1), or not pass (any other key):")
        if failure_code:
            if failure_code == "1":
                grades -= 10
                grade_comments += "minor error with the output image; "
            else:
                grades -= 20
                grade_comments += "failed to detect edge; "

        if not comp_src.endswith("Implementation"+suffix):
            grades -= 1
            grade_comments += "source file name not as specified (-1); "

        record[2] = str(grades)
        record.append(grade_comments)
        writer.writerow(record)
        print record
        #raise SystemExit

