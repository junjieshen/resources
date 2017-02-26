from public import *

# usr/bin/env python
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

for f in glob.glob(prefix+"Lab2-PartB-AssignmentSubmission-manifest.csv"):
        csv_in = f

suffix = ".cpp"
CC = "mpic++"

num_lines = 0
csv_out = prefix+"grades.csv"

comp_binary = prefix+"binary"
cmd_comp_no_src = CC+" -std=c++11 -o "+comp_binary+" "
cmd_run1 = comp_binary+" "+prefix+"aniketsh_input.txt Chapter b1"
cmd_run2 = comp_binary+" "+prefix+"aniketsh_input.txt Chapter b2"

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

        # Grading rubrics
        grades = full_score
        grade_comments = ""

        # Source file
        comp_src = ""
        comp_timelist = []
        
        # Timing report
        report = ""

        files = [ i.strip() for i in record[3].split(";")]
        for f in files:
            ll = [ i.strip() for i in f.split("(")]
            file_name = ll[0]
            eee_time = ll[1][9:-1]
            if file_name.endswith(suffix):
                comp_src = prefix+"Files/"+file_name
                comp_timelist = EEETimeToTimeList(eee_time)
            if file_name.endswith("Timing.pdf"):
                report = prefix+"Files/"+file_name

        if not comp_src:
            if not report:
                grades = 0
                grade_comments += "source file not found; timing report not found; "
            else:
                grades = 10
                grade_comments += "source file not found; "
            record[2] = str(grades)
            record.append(grade_comments)
            print "No source file found for " + record[1] + ", skipping..."
            writer.writerow(record)
            print record
            continue

        if laterThan(comp_timelist, stringToTimeList(args.deadline)):
            grades -= 10
            grade_comments += "overdue (-10); "

        # Try to compile the file
        run(cmd_comp_no_src+comp_src, 10)

        # Check if binary got compiled
        if not os.path.exists(comp_binary):
            if not report:
                grades = 5
                grade_comments += "compilation failed; timing report not found"
            else:
                grades = 15
                grade_comments += "compilation failed; "
            record[2] = str(grades)
            record.append(grade_comments)
            writer.writerow(record)
            print record
            continue

        # Execute the binary
        print
        print "---------> B1"
        res1 = runAndMatch(cmd_run1, 30, "61")
        print
        print "---------> B2"
        res2 = runAndMatch(cmd_run2, 30, "61")

        if (not res1) or (not res2):
            failure_code = raw_input("Please check the results, now choose pass (enter), minor error (1), or not pass (any other key):")
            if failure_code:
                if failure_code == "1":
                    grades -= 5
                    grade_comments += "b1 incorrect result; "
                elif failure_code == "2":
                    grades -= 5
                    grade_comments += "b2 incorrect result; "
                elif failure_code == "3":
                    grades -= 10
                    grade_comments += "incorrect result; "
                elif failure_code == "4":
                    grades -= 10
                    grade_comments += "b1 runtime failure; "
                elif failure_code == "5":
                    grades -= 10
                    grade_comments += "b2 runtime failure; "
                elif failure_code == "6":
                    grades -= 20
                    grade_comments += "b1 and b2 runtime failure; "
                else:
                    grades -= 20
                    grade_comments += failure_code+"; "
            if not report:
                grades -= 10
                grade_comments += "timing report not found; "
            if not comp_src.endswith("ImplementationB"+suffix):
                grades -= 1
                grade_comments += "source file name not as specified (-1); "

        record[2] = str(grades)
        record.append(grade_comments)
        writer.writerow(record)
        print record
#        raise SystemExit

