#!/usr/bin/env python
from public import *

parser = argparse.ArgumentParser(description='Inputs to grade lab assignments.')
parser.add_argument('-d', '--directory', type=str,
        help='The directory to the assignment')
parser.add_argument('-t', '--deadline', type=str,
        help='Deadline of the assignment, in the format of YYYYMMDDHHMMAM or YYYYMMDDHHMMPM')
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

suffix = ".cpp"
CC = "g++-4.8"

num_lines = 0
pgm_out1 = prefix+"out1.pgm"
pgm_out2 = prefix+"out2.pgm"
csv_out = prefix+"grades.csv"

comp_binary = prefix+"binary"
cmd_comp_no_src = CC+" -fopenmp -std=c++11 -o "+comp_binary+" "
cmd_run1 = comp_binary+" "+prefix+"aniketsh_tc1.pgm "+ pgm_out1 + " 25 a1"
cmd_run2 = comp_binary+" "+prefix+"aniketsh_tc1.pgm "+ pgm_out2 + " 25 a2"
cmd_open1 = "feh "+pgm_out1
cmd_open2 = "feh "+pgm_out2

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
        if os.path.exists(pgm_out1):
            os.remove(pgm_out1)
        if os.path.exists(pgm_out2):
            os.remove(pgm_out2)

        # Grading rubrics
        grades = full_score
        grade_comments = ""

        # Source file
        comp_src = ""

        # Analysis report
        report = ""

        files = [ i.strip() for i in record[3].split(";")]
        for f in files:
            ll = [ i.strip() for i in f.split("(")]
            file_name = ll[0]
            eee_time = ll[1][9:-1]
            if file_name.endswith(suffix):
                comp_src = prefix+"Files/"+file_name
            if file_name.endswith(".pdf"):
                report = prefix+"Files/"+file_name

        if not comp_src:
            if not report:
                grades = 0
                grade_comments += "source file not found; timing report not found; "
            else:
                grades = 20
                grade_comments += "source file not found; "
            record[2] = str(grades)
            record.append(grade_comments)
            print "No source file found for " + record[1] + ", skipping..."
            writer.writerow(record)
            print record
            continue

        # Manually checking overdue

        # Try to compile the file
        run(cmd_comp_no_src+comp_src, 10)

        # Check if binary got compiled
        if not os.path.exists(comp_binary):
            grades = 5
            grade_comments += "compilation failed; "
            record[2] = str(grades)
            record.append(grade_comments)
            writer.writerow(record)
            print record
            continue

        # Execute the binary
        run(cmd_run1, 20)
        run(cmd_run2, 20)

        if not report:
            grades -= 20
            grade_comments += "timing report not found; "
        else:
            subprocess.Popen("evince "+report, shell=True)

        if not os.path.exists(pgm_out2):
            grades -= 15
            grade_comments += "a2: no output image generated; "
            print "A2 image not generated"
        else:
            subprocess.Popen(cmd_open2, shell=True)

        # Check if output image exist
        if not os.path.exists(pgm_out1):
            grades -= 15
            grade_comments += "a1: no output image generated; "
            print "A1 image not generated"
        else:
            subprocess.Popen(cmd_open1, shell=True)

        failure_code = raw_input("Please check the results, now choose pass (enter), minor error (1, 2, 3), failed (4, 5, 6), or other reason:")
        if failure_code:
            if failure_code == "1":
                grades -= 5
                grade_comments += "A1: minor error with the output image; "
            if failure_code == "2":
                grades -= 5
                grade_comments += "A2: minor error with the output image; "
            if failure_code == "3":
                grades -= 10
                grade_comments += "A1 & A2: minor error with output images; "
            elif failure_code == "4":
                grades -= 10
                grade_comments += "A1: failed to detect edge; "
            elif failure_code == "5":
                grades -= 10
                grade_comments += "A2: failed to detect edge; "
            elif failure_code == "6":
                grades -= 20
                grade_comments += "A1 & A2: failed to detect edge; "
            else:
                grades -= 20
                grade_comments += failure_code+"; "

        if not comp_src.endswith("Implementation"+suffix):
            grades -= 1
            grade_comments += "source file name not as specified; "

        if report and not report.endswith("Analysis.pdf") and not report.endswith("analysis.pdf"):
            grades -= 1
            grade_comments += "report name not as specified; "

        record[2] = str(grades)
        record.append(grade_comments)
        writer.writerow(record)
        print record
        #raise SystemExit
