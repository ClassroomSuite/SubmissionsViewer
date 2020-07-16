# Update specific files in student repositories
## Use cases

1. Locking specific files from being modified by students (e.g. grading/testing scripts, GitHub actions/workflows)
2. Update specific files in student repositories

Note: It's recommended to update/overwrite important files like grading/testing scripts once an assignment is over to ensure test results are accurate (not altered by students).

## Setup

1. [Select a classroom](https://classroom.github.com/classrooms/)
2. Create or select an existing assignment
3. Add a new autograding test
   * Choose Input/Output test case
   * Copy/Paste the following script into the field <b>Run Command</b>
   * Replace the first line of the script with a link to your own <b>classroom_actions.sh</b> file protected in your original/template repository
4. Finish by selecting <b>Create assignement</b> or <b>Update assignement</b>
 
```bash
wget https://raw.githubusercontent.com/TestOrgJustAymeric/Exercice1/master/scripts/classroom_actions.sh;
chmod -x ./classroom_actions.sh;
bash ./classroom_actions.sh;
```

## How to update/overwrite specific files
1. Add a file named <b>files_to_update.txt</b> to your original/template repository used for your assignement
   * Must be relative to the repository (e.g. [./scripts/files_to_update.txt](../scripts/files_to_update.txt))
2. Add each file you want to update/overwrite in student repositories to [./scripts/files_to_update.txt](../scripts/files_to_update.txt)
```
test_assignement.py
your_module.py
data/your_data.csv
```
3. Commit and push your changes to GitHub
4. [Select your classroom](https://classroom.github.com/classrooms/)
5. Go edit the assignment and select <b>Update assignment</b>

At this point all students should receive your modifications
