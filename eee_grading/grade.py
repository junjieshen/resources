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
ddltimelist = stringToTimeList("201702071155PM")
subtimelist = EEETimeToTimeList("2017-02-06 5:31pm")

os.chdir(args.directory)
for f in glob.glob("*.csv"):
        csv_in = f

prefix = args.directory
if args.directory[-1] != "/":
    prefix += "/"

csv_out = prefix+"grades.csv"
if os.path.exists(csv_out):
    cancelled = raw_input("Do you want to delete the grades? Press enter (delete) or any other key (not delete):")
    if not cancelled:
        os.remove(csv_out)
        num_lines = 0
    else:
        num_lines = sum(1 for line in open(csv_out))

count = 0

writer = csv.writer(open(csv_out, 'a'))

if not csv_in:
    print "No csv found in the directory!"

if args.lang == "c++":
    suffix = ".cpp"
    CC = "g++"
elif args.lang == "c":
    suffix = ".c"
    CC = "gcc"
else:
    print "Unsupported language."
    raise SystemExit

full_score = args.score

comp_binary = "./binary"

with open(csv_in, 'rb') as csvfile:
    submissions = csv.reader(csvfile)
    for record in submissions:
        count += 1
        if (count <= num_lines):
            continue
        if os.path.exists(comp_binary):
            os.remove(comp_binary)
        # Grading rubrics
        grade_no_src = False
        grade_compi_falure = False
        grade_wrong_name = False
        grade_run_failure = False
        grade_overdue = False
        grade_comments = ""
        grades = full_score

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
            grade_no_src = True
            grade_comments += "No source file found; "
            grades = 0
            record[2] = str(grades)
            record.append(grade_comments)
            print "No source file found for " + record[1] + ", skipping..."
            writer.writerow(record)
            continue

        # Try to compile the file
        run(CC+" -pthread -o "+comp_binary+" "+comp_src, 10)

        if not os.path.exists(comp_binary):
            grade_compi_falure = True
            grades = 5
            grade_comments += "compilation failed; "
            record[2] = str(grades)
            record.append(grade_comments)
            writer.writerow(record)
            continue

        # Execute the binary
        run(comp_binary+" 4", 30)
        notPassed = raw_input("Please check the results, now enter pass (enter) or not pass (any other key):")
        if notPassed:
            grade_run_failure = True
            grade_comments += "run failed; "
            grades -= 35

        if not comp_src.endswith("Implementation.c"):
            grade_wrong_name = True
            grades -= 1
            grade_comments += "source file name not as specified (-1); "

        record[2] = str(grades)
        record.append(grade_comments)
        writer.writerow(record)
        print record

