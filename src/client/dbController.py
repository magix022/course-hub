#!/usr/bin/env python3

from audioop import add
from sqlite3 import ProgrammingError
from time import sleep
import psycopg2
from psycopg2.errors import SerializationFailure
from psycopg2 import sql
import json
import logging
import datetime
from psycopg2.extras import UUID_adapter

class CourseHubException(Exception):
    pass


class dbController:

    def __init__(self):
        self.connect()
        self.rowCount = 0
    
    def connect(self):
        self.conn = psycopg2.connect(
            database = 'course-hub-db-5540.coursehub',
            user = '',
            host = 'free-tier.gcp-us-central1.cockroachlabs.cloud',
            port = 26257,
            password = ''
        )

    def cursor(self):
        return self.conn.cursor()

    def updateRowCount(self, rowCount):
        self.rowCount = rowCount
    
    def getRowCount(self):
        return self.rowCount

    def setRowCount(self, c):
        self.rowCount = c

    def adaptUUID(self, uuid):
        return UUID_adapter(uuid)

    def retryCommit(self):
        n = 0
        max_retries = 6
        while True:
            n += 1
            if n == max_retries:
                raise psycopg2.Error("did not succed within N retries")
            try:
                self.conn.commit()
                break
            except psycopg2.Error as e:
                if e.pgcode != 40001:
                    raise psycopg2.Error()
                else:
                    self.conn.rollback()
                    sleep(0.5)

    def close(self):
        self.conn.close()


    def add_course(self,disc):
        if(self.conn.closed != 0):
            self.connect()
        #
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    """INSERT INTO courses (subject, courseNb, title, crn, semester, type, credit, year,
                    section, location, monday, tuesday, wednesday, thursday, friday, instructor, startTime, endTime) 
                    VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
                        disc["subject"], #0
                        #faculty         #1
                        disc["courseNb"], #2
                        disc["title"], #3
                        disc["crn"], #4
                        disc["semester"], #5
                        disc["type"], #6
                        disc["credit"], #7
                        disc["year"], #8
                        disc["section"], #9
                        disc["location"], #10
                        disc["monday"], #11
                        disc["tuesday"], #12
                        disc["wednesday"], #13
                        disc["thursday"], #14
                        disc["friday"], #15
                        disc["instructor"], #16
                        disc["startTime"], #17
                        disc["endTime"] #18
                    )
                )
            except psycopg2.errors.UniqueViolation as e:
                self.conn.rollback()
                raise psycopg2.errors.UniqueViolation
            
            self.updateRowCount(cur.rowcount)
            logging.debug("add_course(): status message: %s", cur.statusmessage)
        self.retryCommit()

    def delete_course(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM courses WHERE crn = %s", (crn, )
            )
            self.delete_course_assignments(crn)
            self.delete_course_exams(crn)
            self.updateRowCount(cur.rowcount)
        self.retryCommit()

    def add_user(self, disc): #NEED TO HANDLE NON_UNIQUE EMAIL IN APP
        if(self.conn.closed != 0):
            self.connect()
        
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO users (firstname, lastname, email, studentid) VALUES (%s, %s, %s, %s)",(
                        disc["firstname"],
                        disc["lastname"],
                        disc["email"],
                        disc["studentid"]
                    )
                )
            except psycopg2.errors.UniqueViolation as e:
                self.conn.rollback()
                raise psycopg2.errors.UniqueViolation
            
            self.updateRowCount(cur.rowcount)
            logging.debug("add_user(): status nmessage: %s", cur.statusmessage)
        self.retryCommit()

    def delete_user(self, email):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE email = %s",(email,)
            )
            self.delete_user_registeredClasses(email)
            self.updateRowCount(cur.rowcount)
            logging.debug("delete_user(): status message: %s", cur.statusmessage)
        self.retryCommit()

    def get_user(self, email):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE email = %s", (email,)
            )
            self.updateRowCount(cur.rowcount)
            return cur.fetchone()

    def get_user_exams(self, email):
        if(self.conn.closed):
            self.connect()
        courseList = self.getRegisteredClasses(email)
        examsList = []
        crnList = []
        for course in courseList:
            crnList.append(course[5])
        tup = tuple(crnList)
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM exams WHERE courseCRN in %s", (tup,)
            )
            try:
                examsList = cur.fetchall()
            except ProgrammingError:
                self.conn.rollback()
                raise CourseHubException("No exams for given users")
            
        return examsList

    def get_user_assignments(self, email):
        if(self.conn.closed):
            self.connect()
        courseList = self.getRegisteredClasses(email)
        assList = []
        for course in courseList:
            assignmentsList = self.get_course_assignments(course[5])
            for ass in assignmentsList:
                assList.append(ass)
        return assList


        
    
    def add_assignment(self, disc):
        if(self.conn.closed):
            self.connect()
        
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO assignments (name, dueDate, dueTime, submissionPlatform, submissionPlatformURL, courseCRN)
                 VALUES ( %s,%s,%s,%s,%s,%s) RETURNING assignmentid""",(
                    disc["name"],
                    disc["dueDate"],
                    disc["dueTime"],
                    disc["submissionPlatform"],
                    disc["submissionPlatformURL"],
                    disc["courseCRN"]
                )
            )
            id = cur.fetchone()[0]
            
            self.updateRowCount(cur.rowcount)
            logging.debug("add_assignment(): status message: %s", cur.statusmessage)
        self.retryCommit()
        return id

    def delete_assignment(self, id):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM assignments WHERE assignmentid = %s", (id, )
            )
            self.updateRowCount(cur.rowcount)
        logging.debug("delete_assignment(): status message: %s ", cur.statusmessage)
        self.retryCommit()

    def delete_course_assignments(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM assignments WHERE courseCRN = %s", (crn,)
            )
            self.updateRowCount(cur.rowcount)
        self.retryCommit()
    
    def get_course_assignments(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM assignments WHERE courseCRN = %s", (crn,)
            )
            try:
                assList = cur.fetchall()
            except ProgrammingError:
                self.conn.rollback()
                raise CourseHubException("No assignments for given course crn")
        return assList

    def get_course_exams(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM exams WHERE courseCRN = %s", (crn,)
            )
            try:
                examList = cur.fetchall()
            except ProgrammingError:
                self.conn.rollback()
                raise CourseHubException("No exams for given course crn")
        return examList


    def add_exam(self, disc):
        if(self.conn.closed):
            self.connect()
        
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO exams (weight, type, date, time, location, duration, courseCRN)
                VALUES ( %s,%s,%s,%s,%s,%s,%s) RETURNING examid""",(
                    disc["weight"],
                    disc["type"],
                    disc["date"],
                    disc["time"],
                    disc["location"],
                    disc["duration"],
                    disc["courseCRN"]
                )
            )
            id = cur.fetchone()[0]

            self.updateRowCount(cur.rowcount)
            logging.debug("add_exam(): status message: %s", cur.statusmessage)
        self.retryCommit()
        return id

    def delete_exam(self, id):
        if(self.conn.closed):
            self.connect()

        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM exams WHERE examid = %s", (id, )
            )
            self.updateRowCount(cur.rowcount)
            logging.debug("delete_exam(): status message: %s", cur.statusmessage)
        self.retryCommit()

    def delete_course_exams(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM exams WHERE courseCRN = %s", (crn,)
            )
            self.updateRowCount(cur.rowcount)
        self.retryCommit()

    def getCourse(self, crn):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            try:
                cur.execute("SELECT * FROM courses WHERE crn = %s", (crn,))
                res = cur.fetchone()            
            except ProgrammingError as e:
                self.conn.rollback()
                raise CourseHubException("No course for given crn")
            
            self.updateRowCount(cur.rowcount)
            return res

    def add_registeredClass(self, email, crn):
        if(self.conn.close):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE email = %s", (email,)
            )
            try:
                cur.fetchone()
            except ProgrammingError as e:
                self.conn.rollback()
                raise CourseHubException("No user associated with specified email")

            cur.execute(
                "SELECT * FROM courses WHERE crn = %s", (crn,)
            )
            try:
                cur.fetchone()
            except ProgrammingError as e:
                self.conn.rollback()
                raise CourseHubException("No course associated with specified CRN")

            cur.execute(
                "INSERT INTO registeredClass (email, crn) VALUES (%s,%s) RETURNING id",(
                    email, crn
                )
            )
            self.updateRowCount(cur.rowcount)
            id = cur.fetchone()[0]
        self.retryCommit()
        return id

    def delete_registeredClass(self, email, crn):
        if(self.conn.close):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM registeredClass WHERE email = %s AND crn = %s", (email, crn)
            )
            self.updateRowCount(cur.rowcount)
        self.retryCommit()

    def delete_user_registeredClasses(self, email):
        if(self.conn.closed):
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM registeredclass WHERE email = %s", (email,)
            )
            self.updateRowCount(cur.rowcount)
        self.retryCommit()

    def getRegisteredClasses(self, email):
        if(self.conn.close):
            self.connect()
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM registeredClass WHERE email = %s ORDER BY crn", (email, )
                )
                rows = cur.fetchall()
            except ProgrammingError as e:
                self.conn.rollback()
                raise CourseHubException("No registered class for given user")
            courseList = []
            for row in rows:
                courseList.append(self.getCourse(row[2]))

            return courseList

    def main(self):
        self.connect()
        x = {
            "firstname": "John",
            "lastname": "doe",
            "email": "jon@doe",
            "studentid": 433421
        }
        y = json.dumps(x)
        self.add_user(y)
        #self.delete_user("jon@doe")
        print("Connected")
        print(self.conn.closed)
        self.conn.close()


if __name__ == "__main__":
    controller = dbController()
    controller.main()

    
