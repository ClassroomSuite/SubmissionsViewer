# DEPRECATED
# Show autograding scores in README
Update autograding results on each push/pull.

Results are shown in [README.md](../README.md).

*Note: Make sure the [update/overwrite student repositories script](update_student_repositories.md) runs before this script to avoid potential overwriting of student README files after applying the grading scores.*

## Setup

1. [Select a classroom](https://classroom.github.com/classrooms/)
2. Create or select an existing assignment
3. Add a new autograding test
   * Choose Input/Output test case
   * Copy/Paste the following script into the field <b>Run Command</b>
   * Replace the first two lines of the script with your <b>repository name</b> (the original/template repository)
     and with the git clone <b>repository link</b>
4. Finish by selecting <b>Create assignment</b> or <b>Update assignment</b>
 
```bash
git config --local user.email "action@github.com";
git config --local user.name "GitHub Action";
python3 test_exercice.py;
python3 scripts/show_grades_in_readme.py;
git add logs/tests_results.txt;
git add README.md;
git commit -a -m "Updated autograding results";
git push;
echo 0;
```
``
