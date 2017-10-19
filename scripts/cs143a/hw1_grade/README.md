## Shell Grading Scripts

Grading automation customized to UCI Canvas.

### Usage

1. Replace the roster file with the one downloaded from Canvas.

    Similar the template included, add a column of index for each students. Starting from 1.


2. Download the submission zip file from Canvas and put it in the same directory as the scripts.


2. Choose the group which you are responsible for.

    Replace the line 37 in `grade_group.sh` with either group1, 2, or 3.


3. Run.

    ```
    ./grade_group.sh
    ```

    The grades will be written in a file called `group_grades.csv`

    Simply open the file with Excel and copy the scores to the common gradebook. 

### Note

* Tests are presented under `./tests`.
* The point distribution is explained in `grade_one.py`.
* Extra credits are not graded. But the CSV file will have a field indicating whether this student implemented the extra part or not.
* To double check the score, please change directory to `./results/student_index`. All the source files and test files should already be copied there.
* **I didn't handle zip file submissions, so please check manually!!!**
