from dataclasses import dataclass, field, asdict
import json
import course_scrape as cs
import mycourses_scrape as ms
from datetime import datetime, time, date, timedelta
from dbController import *




@dataclass(slots=True)
class Events:
    course: str = ""
    type: str = ""
    deadline: datetime.date = ""
    length: timedelta = ""
    title: str = ""
    date: datetime.date = ""
    text: str = ""


@dataclass(slots=True)
class Assignment:
    name: str = ""
    title: str = ""
    type: str = ""
    dueDate: str = ""
    dueTime: str = ""
    date: str = ""
    crn: int = 0


@dataclass(slots=True)
class Exam:
    weight: int = 0
    type: str = ""
    date: datetime.datetime = datetime.datetime(2000, 1, 1)
    time: datetime.time = datetime.time(0, 0, 0)
    title: str = ""
    location: str = ""
    duration: datetime.timedelta = datetime.timedelta(0, 0)
    courseCRN: int = 0


@dataclass(slots=True)
class Course:
    courseid: int = 0
    subject: str = ""
    courseNb: int = 0
    title: str = ""
    crn: int = 0
    semester: str = ""
    type: str = ""
    credit: int = 0
    year: int = 0
    section: str = ""
    location: str = ""
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    instructor: str = ""
    startTime: time = time
    endTime: time = time
    events: list = field(default_factory=list)
    assignments: list = field(default_factory=list)
    exams: list = field(default_factory=list)

    def add_event(self, event):
        self.evens.append(event)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def add_exam(self, exam):
        self.exams.append(exam)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass(slots=True)
class User:
    firstname: str = ""
    lastname: str = ""
    email: str = ""
    studentid: int = 0
    courses: list = field(default_factory=list)

    def get_courses(self):
        return self.courses

    def add_course(self, course):
        self.courses.append(course)

    def to_json(self):
        return json.dumps(asdict(self))


# Helpers

def find_days(course, days):
    if "M" in days:
        course.monday = True
    if "T" in days:
        course.tuesday = True
    if "W" in days:
        course.wednesday = True
    if "R" in days:
        course.thursday = True
    if "F" in days:
        course.friday = True


def find_times(course, times):
    new_times = times.split(" - ")
    start_time_hour = new_times[0].split(" ")[0].split(":")[0]
    start_time_min = new_times[0].split(" ")[0].split(":")[1]
    start_time_noon = new_times[0].split(" ")[1]
    end_time_hour = new_times[1].split(" ")[0].split(":")[0]
    end_time_min = new_times[1].split(" ")[0].split(":")[1]
    end_time_noon = new_times[1].split(" ")[1]

    if start_time_noon == "am" or (start_time_noon == "pm" and start_time_hour == "12"):
        start_time = f"{start_time_hour}:{start_time_min}"
        course.startTime = datetime.datetime.strptime(start_time, "%H:%M").time()

    else:
        start_time = f"{str(int(start_time_hour) + 12)}:{start_time_min}"
        course.startTime = datetime.datetime.strptime(start_time, "%H:%M").time()

    if end_time_noon == "am" or (end_time_noon == "pm" and end_time_hour == "12"):
        end_time = f"{end_time_hour}:{end_time_min}"
        course.endTime = datetime.datetime.strptime(end_time, "%H:%M").time()

    else:
        end_time = f"{str(int(end_time_hour) + 12)}:{end_time_min}"
        course.endTime = datetime.datetime.strptime(end_time, "%H:%M").time()


def course_information_helper(course_list):
    new_course_list = []

    for course in course_list:
        new_course = Course()
        find_days(new_course, course["day"])
        find_times(new_course, course["times"])
        new_course.subject = course["subject"][1:5]
        new_course.courseNb = int(course["subject"][6:9])
        new_course.title = course["title"][:-1]
        new_course.crn = int(course["crn"])
        new_course.semester = course["term"][:-5]
        new_course.type = course["type"]
        new_course.credit = int(course["credits"][0:1])
        new_course.year = int(course["term"][len(course["term"]) - 4:])
        new_course.section = course["section"][1:]
        new_course.location = course["location"]

        if "instructor" in course:
            new_course.instructor = course["instructor"]

        else:
            new_course.instructor = course["instructors"]

        new_course_list.append(asdict(new_course))

    return new_course_list


# dict must contain: {"firstname": "", "lastname": "", "studentid": "", "email": "", "password": ""}
# firstname, lastname and studentid are redundant -> only really need email to identify user
def get_course_information(user_dict):
    db = dbController()

    # try to add user if he isn't in the database already
    try:
        db.add_user(user_dict)
    except psycopg2.errors.UniqueViolation:
        pass

    # try to see if there is already registered courses for this user in the database

    registered_classes = db.getRegisteredClasses(user_dict["email"])

    if len(registered_classes) == 0:
        course_list = cs.get_schedule(user_dict["email"], user_dict["password"])
        new_course_list = course_information_helper(course_list)

        # add courses to the database if they are not already there
        for course in new_course_list:
            try:
                db.add_course(course)
            except psycopg2.errors.UniqueViolation:
                pass
            try:
                db.add_registeredClass(user_dict["email"], course["crn"])
            except:
                pass

        registered_classes = db.getRegisteredClasses(user_dict["email"])

    final_courses = []

    for course in registered_classes:
        id, subject, _, *other = course
        final_courses.append(asdict(Course(*(id, subject, *other))))

    return final_courses


# dict must contain: {"firstname": "", "lastname": "", "studentid": "", "email": "", "password": ""}
def get_event_information(user_dict, course_list, crn_dict):
    db = dbController()
    email = user_dict['email']

    # try to add user if he isn't in the database already
    try:
        db.add_user(user_dict)
    except psycopg2.errors.UniqueViolation:
        pass

    exams = db.get_user_exams(email)
    if len(exams) == 0:

        events = ms.get_events(course_list, email, password)

        for event in events:
            new_exam = Exam()
            new_exam.course = event["subject"]
            new_exam.type = event["type"]
            new_exam.date = event["deadline"]
            new_exam.location = event["title"]
            new_exam.courseCRN = crn_dict[event["subject"]]

            db.add_exam(asdict(new_exam))

        exams = db.get_user_exams(email)

    final_exams = []

    for exam in exams:
        final_exam = Exam()
        final_exam.type = exam[3]
        final_exam.date = exam[4]
        final_exam.title = exam[6]
        final_exam.courseCRN = exam[8]
        final_exams.append(asdict(final_exam))

    return final_exams


if __name__ == "__main__":
    # example_dict = {"firstname": "John", "lastname": "Doe", "studentid": "123", "email": email, "password": password}

    # print(get_information(example_dict))
    # secrets = open("../../assets/secrets.txt").readlines()
    # email = secrets[0][:-1]
    # password = secrets[1]

    print(
        get_event_information({"firstname": "", "lastname": "", "studentid": 123, "email": email, "password": password},
                              ["BIOL-568", "COMP-321", "COMP-424", "COMP-564", "MATH-324"],
                              {"BIOL-568": 1878, "COMP-321": 2215, "COMP-424": 2225, "COMP-564": 2233,
                               "MATH-324": 3406}))
    # print(ms.get_events(["BIOL-568", "COMP-321", "COMP-424", "COMP-564", "MATH-324"], email, password))
