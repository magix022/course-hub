# course-hub
As college students, we have always struggled to find an efficient way to track the constant flow of assignments, quizzes, midterms, etc. Upon launch, Course Hub automatically retrieves and interprets new course information on McGill's websites (MyCourses and Minerva). This information is then added to the Course Hub calendar, which is fully editable. Our app also fetches and displays the student's schedule. **This was a project for the McHacks 2022 hackathon**
## HOW TO USE
### 1. install the python environment dependencies using the requirements.txt in the assets folder

```
conda create --name <my_env_name> --file ./assets/requirements.txt
```
or 
```
pip install -r ./assets/requirements.txt
```
### 2. run the weekly_schedule.py in the client directory

```
python weekly_schedule.py
```

