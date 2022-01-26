import datetime
import pytest
from server.dbController import *
import uuid

def test_addDeletecourse():
    controller = dbController()
    x= {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    ass1 = {
        "name": "ass1",
        "dueDate": datetime.date(2022,1,1),
        "dueTime": datetime.time(12,00),
        "submissionPlatform": "ed",
        "submissionPlatformURL": "lkin",
        "courseCRN": 250
    }
    ass2 = {
        "name": "ass2",
        "dueDate": datetime.date(2022,1,1),
        "dueTime": datetime.time(12,00),
        "submissionPlatform": "ed",
        "submissionPlatformURL": "lkin",
        "courseCRN": 250
    }
    exam1 = {
        "weight": 30,
        "type": "quiz",
        "date": datetime.date(2022, 1, 1),
        "time": datetime.time(12,0),
        "location": "building",
        "duration": datetime.timedelta(hours=3),
        "courseCRN": 250
    }
    exam2 = {
        "weight": 30,
        "type": "quiz",
        "date": datetime.date(2022, 1, 1),
        "time": datetime.time(12,0),
        "location": "building",
        "duration": datetime.timedelta(hours=3),
        "courseCRN": 250
    }
    controller.add_course(x)
    assert controller.getRowCount() == 1
    controller.add_assignment(ass1)
    controller.add_assignment(ass2)
    controller.add_exam(exam1)
    controller.add_exam(exam2)

    controller.setRowCount(0)
    controller.delete_course(250)
    assert controller.getRowCount() == 1

    cur = controller.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM assignments WHERE courseCRN = %s", (250,)
    )
    assert cur.fetchone()[0] == 0

    cur = controller.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM exams WHERE courseCRN = %s", (250,)
    )
    assert cur.fetchone()[0] == 0


def test_addDeleteUser():
    controller = dbController()
    x = {
        "firstname": "John",
        "lastname": "doe",
        "email": "jon@doe",
        "studentid": 433421
    }
    course = {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    controller.add_user(x)
    assert controller.getRowCount() == 1
    controller.add_course(course)
    controller.add_registeredClass("jon@doe", 250)

    controller.setRowCount(0)
    controller.delete_user("jon@doe")
    assert controller.getRowCount() == 1

    cur = controller.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM registeredclass WHERE email = %s", ("jon@doe",)
    )
    assert cur.fetchone()[0] == 0

    controller.delete_course(250)

def test_addDeleteAssignment():
    controller = dbController()
    x = {
        "name": "assignment",
        "dueDate": datetime.date(2022,1,24),
        "dueTime": datetime.time(12,00),
        "submissionPlatform": "ed",
        "submissionPlatformURL": "lkin",
        "courseCRN": 3367
    }
    id = controller.add_assignment(x)
    assert controller.getRowCount() == 1
    #controller.setRowCount(0)
    controller.delete_assignment(id)
    #assert controller.getRowCount() == 1
    #controller.setRowCount(0)

def test_addDeleteExam():
    controller = dbController()
    id = controller.adaptUUID(uuid.uuid4())
    x = {
        "weight": 30,
        "type": "quiz",
        "date": datetime.date(2022, 1, 12),
        "time": datetime.time(12,0),
        "location": "building",
        "duration": datetime.timedelta(hours=3),
        "courseCRN": 3411
    }
    id = controller.add_exam(x)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    #controller.delete_exam(id)
    #assert controller.getRowCount() == 1

def test_getCourse():
    controller = dbController()
    x= {
        "subject": "comp",
        #faculty
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    controller.add_course(x)
    course = controller.getCourse(250)
    assert course[5] == 250
    assert course[1] == "comp"
    assert course[3] == 250
    assert course[4] == "Intro to computer science"
    controller.delete_course(250)
    assert controller.getRowCount() == 1

def test_addDeleteRegClass():
    controller = dbController()
    course = {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    user = {
        "firstname": "John",
        "lastname": "doe",
        "email": "jon@doe",
        "studentid": 433421
    }
    controller.add_registeredClass("jon@doe", 250)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    controller.delete_registeredClass("jon@doe", 250)
    assert controller.getRowCount() == 1

def test_getRegisteredClasses():
    controller = dbController()
    course1 = {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    course2 = {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":251,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    course3 = {
        "subject": "comp",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":252,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    controller.add_course(course1)
    controller.add_course(course2)
    controller.add_course(course3)
    user = {
        "firstname": "John",
        "lastname": "doe",
        "email": "jon@doe",
        "studentid": 433421
    }
    controller.add_user(user)
    controller.add_registeredClass("jon@doe", 250)
    controller.add_registeredClass("jon@doe", 251)
    controller.add_registeredClass("jon@doe", 252)
    courseList = controller.getRegisteredClasses("jon@doe")
    controller.delete_course(250)
    controller.delete_course(251)
    controller.delete_course(252)
    controller.delete_user("jon@doe")
    controller.delete_registeredClass("jon@doe", 250)
    controller.delete_registeredClass("jon@doe", 251)
    controller.delete_registeredClass("jon@doe", 252)

    assert (courseList[0])[5] == 250
    assert (courseList[1])[5] == 251
    assert (courseList[2])[5] == 252

def test_getUser():
    controller = dbController()
    user = {
        "firstname": "John",
        "lastname": "doe",
        "email": "jon@doe",
        "studentid": 433421
    }

    controller.add_user(user)
    user = controller.get_user("jon@doe")
    controller.delete_user("jon@doe")
    assert user[1] == "John"
    assert user[2] == "doe"
    assert user[3] == "jon@doe"
    assert user[4] == 433421


    

    

