import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

user_dict = [{"courseid": "0c7c5316-8eef-433c-87bb-971ac91e1122", "subject": "BIOL", "courseNb": 568,
              "title": "Topics on the Human Genome", "crn": 1878, "semester": "Winter", "type": "Lecture",
              "credit": 3, "year": 2022, "section": 1, "location": "Stewart Biology Building S3/4", "monday": False,
              "tuesday": True, "wednesday": False, "thursday": True, "friday": False,
              "instructor": "James Engert, Swneke D Bailey, Livia Garzia, David Langlais, Sampath Kumar Loganathan,"
                            " Alexandre Montpetit, Joanna Przybyl, Jean-Baptiste Riviere, Hamed Shateri Najafabadi,"
                            " Rima Slim, George Thanassoulis, Yojiro Yamanaka, Ma'n Hilmi M Zawati",
              "startTime": "16:05", "endTime": "17:25", "events": [{"course": "BIOL 568", "type": "assignment 1",
                                                                    "deadline": "February 1st", "length": 0,
                                                                    "title": "New Assignment", "date": "January 15th",
                                                                    "text": "Ayo new assignment just dropped"}],
              "exams": []},
             {"courseid": "0d8f4b58-0803-4ea9-9cbc-bd1ede8f961b", "subject": "COMP", "courseNb": 321,
              "title": "Programming Challenges", "crn": 2215, "semester": "Winter", "type": "Lecture", "credit": 1,
              "year": 2022, "section": 1, "location": "Adams Building AUD", "monday": False, "tuesday": False,
              "wednesday": True, "thursday": False, "friday": False, "instructor": "David C Becerra",
              "startTime": "11:35", "endTime": "12:25", "events": [{"course": "COMP 321", "type": "assignment 1",
                                                                    "deadline": "February 1st", "length": 0,
                                                                    "title": "New Assignment", "date": "January 15th",
                                                                    "text": "Ayo new assignment just dropped"}], "exams": []},
             {"courseid": "51baa2e4-2f78-4d6a-9290-4f35021cc67e", "subject": "COMP", "courseNb": 424,
              "title": "Artificial Intelligence", "crn": 2225, "semester": "Winter", "type": "Lecture", "credit": 3,
              "year": 2022, "section": 1, "location": "TBA", "monday": False, "tuesday": False, "wednesday": True,
              "thursday": False, "friday": True, "instructor": "Jackie Cheung, Bogdan Mazoure", "startTime": "16:05",
              "endTime": "17:25", "events": [{"course": "COMP 424", "type": "assignment 1",
                                                                    "deadline": "February 1st", "length": 0,
                                                                    "title": "New Assignment", "date": "January 15th",
                                                                    "text": "Ayo new assignment just dropped"}], "exams": []},
             {"courseid": "78e3bf10-a00d-4600-be89-7c19044b4f78",
              "subject": "COMP", "courseNb": 564, "title": "Advanced Computational Biology Methods and Research",
              "crn": 2233, "semester": "Winter", "type": "Lecture", "credit": 3, "year": 2022, "section": 1,
              "location": "Stewart Biology Building S3/3", "monday": False, "tuesday": True, "wednesday": False,
              "thursday": True, "friday": False, "instructor": "Jérome Waldispuhl", "startTime": "10:05",
              "endTime": "11:25", "events": [{"course": "COMP 564", "type": "assignment 1",
                                                                    "deadline": "February 1st", "length": 0,
                                                                    "title": "New Assignment", "date": "January 15th",
                                                                    "text": "Ayo new assignment just dropped"}], "exams": []},
             {"courseid": "d894caf5-a816-4a92-b33f-d8ce3c06e0b3", "subject": "MATH", "courseNb": 324,
              "title": "Statistics", "crn": 3406, "semester": "Winter", "type": "Lecture", "credit": 3, "year": 2022,
              "section": 1, "location": "TBA", "monday": True, "tuesday": False, "wednesday": True, "thursday": False,
              "friday": True, "instructor": "Yi Yang", "startTime": "08:35", "endTime": "09:25",
              "events": [{"course": "MATH 324", "type": "assignment 1",
                                                                    "deadline": "February 1st", "length": 0,
                                                                    "title": "New Assignment", "date": "January 15th",
                                                                    "text": "Ayo new assignment just dropped"}], "exams": []}]


class User:
    def __init__(self, courses):
        self.courses = courses


class Ui(QWidget):

    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.setFixedSize(900, 500)

        self.width = 900
        self.height = 500

        self.setFixedSize(self.width, self.height)

        '''MENU ON THE MAIN WINDOW'''
        self.menu = QStackedLayout()

        self.howToMenu = QWidget()

        self.howToMenuUi()
        self.menu.addWidget(self.howToMenu)

    def howToMenuUi(self):
        self.howToMenu_layout = QGridLayout()

        self.howToMenu.setFixedSize(self.width, self.height)

        self.howToTitle = QLabel()
        self.howToTitle.setGeometry(QRect(10, 50, self.width, 40))
        self.howToTitle.setStyleSheet("font: 14pt Century Gothic")
        self.howToTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.howToTitle.setText("Courses")

        self.howToSteps = QListWidget()
        self.howToSteps.setGeometry(QRect(10, 150, 200, 80))
        for course in user_dict:
            item = QListWidgetItem(f"{course['subject']} {course['courseNb']}")
            self.howToSteps.insertItem(0, item)
        self.howToSteps.currentRowChanged.connect(self.display_traverse)

        self.course1 = QWidget()
        self.course2 = QWidget()
        self.course3 = QWidget()
        self.course4 = QWidget()
        self.course5 = QWidget()

        self.course1Ui()
        self.course2Ui()
        self.course3Ui()
        self.course4Ui()
        self.course5Ui()

        self.traverse_action = QStackedWidget()
        self.traverse_action.addWidget(self.course1)
        self.traverse_action.addWidget(self.course2)
        self.traverse_action.addWidget(self.course3)
        self.traverse_action.addWidget(self.course4)
        self.traverse_action.addWidget(self.course5)
        self.traverse_action.setCurrentIndex(0)

        self.howToMenu_left_layout = QVBoxLayout()
        self.howToMenu_left_layout.addWidget(self.howToTitle)
        self.howToMenu_left_layout.addWidget(self.howToSteps)

        self.howToMenu_layout.addLayout(self.howToMenu_left_layout, 0, 0, 1, 1)
        self.howToMenu_layout.addWidget(self.traverse_action, 0, 1, 1, 1)
        self.howToMenu.setLayout(self.howToMenu_layout)


    def course1Ui(self):
        self.course1layout = QVBoxLayout()
        self.course1list = QListWidget()
        for event in user_dict[0]["events"]:
            self.course1list.addItem(event)
        self.course1layout.addWidget(self.course1list)
        self.course1.setLayout(self.course1layout)

    def course2Ui(self):
        self.course2layout = QVBoxLayout()
        self.course2list = QListWidget()
        for event in user_dict[1]["events"]:
            self.course2list.addItem(event)
        self.course2layout.addWidget(self.course2list)
        self.course2.setLayout(self.course2layout)

    def course3Ui(self):
        self.course3layout = QVBoxLayout()
        self.course3list = QListWidget()
        for event in user_dict[2]["events"]:
            self.course3list.addItem(event)
        self.course3layout.addWidget(self.course3list)
        self.course3.setLayout(self.course3layout)

    def course4Ui(self):
        self.course4layout = QVBoxLayout()
        self.course4list = QListWidget()
        for event in user_dict[3]["events"]:
            self.course4list.addItem(event)
        self.course4layout.addWidget(self.course4list)
        self.course4.setLayout(self.course4layout)

    def course5Ui(self):
        self.course5layout = QVBoxLayout()
        self.course5list = QListWidget()
        for event in user_dict[4]["events"]:
            self.course5list.addItem(event)
        self.course5layout.addWidget(self.course5list)
        self.course5.setLayout(self.course5layout)

    def display_traverse(self, index):
        self.traverse_action.setCurrentIndex(index)


class Main(QMainWindow, Ui):

    def __init__(self):
        super(Main, self).__init__()

        self.setupUi(self)

    def menuWindow(self):
        self.menu.setCurrentIndex(0)

    def howToWindow(self):
        self.menu.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = Main()
    sys.exit(app.exec())
