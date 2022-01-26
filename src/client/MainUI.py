from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from itertools import chain, repeat
from dataclasses import dataclass, field
from enum import IntEnum
from os import path
from typing import Any
from monthlyCalendar import calendarFrame
from interpret_raw_data import get_course_information, get_event_information
from datetime import date
from tasksalert import TasksView
from login import Login

'''nicholas.corneau@mail.mcgill.ca

'''

__DEBUG__ = True


@dataclass(slots=True)
class User:
	email: str = ""
	pw: str = ""
	courses: list[dict[str, Any]] = field(default_factory=list)

	@property
	def user_dict(self):
		return {"firstname": "", "lastname": "", 
				"studentid": 123, "email": self.email, "password": self.pw}


file_dir = path.dirname(path.realpath(__file__))
assets_dir = file_dir+"/../../assets/icons/"

'''
ENUMS
'''
class EntryKind(IntEnum):
	COURSE = 0
	TUTORIAL = 1
	LAB = 2
	CUSTOM = 3


DAYS_MAP = {day:i for i,day in enumerate(('M', 'T', 'W', 'R', 'F'))}


def getCRNDict(courses):
	crn_map = {}
	for course in courses:
		course_name = course['subject']+"-"+course["courseNb"]
		crn_map[course_name] = int(course["crn"])
	return crn_map


class MainTabs(QTabWidget):
	def __init__(self, user, master=None):
		QTabWidget.__init__(self, master)
		self.user = user
		self.insertCalendar()
		self.tasks = TasksView()
		self.insertTasks(self.tasks)
		self.setMinimumWidth(1280)
		self.setMinimumHeight(720)
		self.insertMonthly()
		self.tabBar().setIconSize(QSize(70,70))
		self.setCornerIcon()


	def fixTabIcons(self):
		for i in range(self.count()):
			self.setCurrentIndex(i)
		self.setCurrentIndex(0)

	def requestNewEvents(self):
		events = get_event_information(
			self.user.user_dict, (courses := self.user.courses), getCRNDict(courses)
			)
		for event in events:
			self.tasks.addTask(event)


	def insertCalendar(self):
		self.calendar = ScheduleTab()
		calIcon = QIcon()
		print(assets_dir+"calendar_grayed.png")
		calIcon.addFile(assets_dir+"calendar_grayed.png", QSize(40, 40), QIcon.Normal, QIcon.Off);
		calIcon.addFile(assets_dir+"calendar_subtle_glow.png", QSize(40, 40), QIcon.Normal, QIcon.On);
		self.addTab(self.calendar, calIcon, "")


	def insertTasks(self, widget=None):
		if widget is None:
			widget = QWidget()
		taskIcon = QIcon()
		taskIcon.addFile(assets_dir+"tasks_unselected.png", QSize(10, 10), QIcon.Normal, QIcon.Off);
		taskIcon.addFile(assets_dir+"tasks_subtle_glow.png", QSize(10, 10), QIcon.Normal, QIcon.On);
		self.addTab(widget, taskIcon, "")


	def insertMonthly(self):
		taskIcon = QIcon()
		taskIcon.addFile(assets_dir+"tasks_unselected.png", QSize(10, 10), QIcon.Normal, QIcon.Off);
		taskIcon.addFile(assets_dir+"tasks_subtle_glow.png", QSize(10, 10), QIcon.Normal, QIcon.On);
		calFrame = calendarFrame(self.user.email)
		self.addTab(calFrame.getWidget(), taskIcon, "")

	def setCornerIcon(self):
		logo = QIcon()
		# print(assets_dir+"logo-padded-test.png")
		logo.addFile(assets_dir+"logo-padded-test.png", QSize(200,100))
		logoWidget = QLabel()
		logoWidget.setMinimumSize(300,20)
		# sizer = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		# sizer.setControlType(QSizePolicy.Expanding)
		# logoWidget.setSizePolicy(sizer);
		logoWidget.setPixmap(logo.pixmap(QSize(300,160)))
		self.setCornerWidget(logoWidget, Qt.TopLeftCorner)




class Entry(QTableWidgetItem):
	# def __init__(self, start, duration, days, kind):
	# 	QTableWidgetItem.__init__(self)
	# 	self.start = start
	# 	self.duration = duration
	# 	self.days = days
	# 	self.kind = kind
	def __init__(self, name, kind, color=None):
		QTableWidgetItem.__init__(self)
		self.kind = kind
		self.name = name
		self.setText(name)
		# color = QColor(220, 70, 70) if color is None else color
		self.setForeground(QColor("White"))
		# QTableWidgetItem.setTextColor(self, QColor("white"))
		self.setBackground(QColor(220, 70, 70))
		self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.entry_data = {}

	def setInfo(self, data):
		self.entry_data = data

	def copy(self):
		new = Entry(self.name, self.kind)
		new.entry_data = self.entry_data
		return new


def get_am_pm():
	# suffix = 'AM' if am else 'PM'
	times = []
	for suffix in ('AM', 'PM'):
		for i in chain((12,), range(1, 12)):
			times.append(f"{i}:00 {suffix}")
			times.append(f"{i}:30 {suffix}")
	return times



class ScheduleTab(QTableWidget):
	def __init__(self, master=None):
		QTableWidget.__init__(self, master)
		self.createWeeklyCal()

		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

	def createWeeklyCal(self):
		self.setColumnCount(7)
		self.setRowCount(48)
		self.setHorizontalHeaderLabels(
				("Sunday", "Monday", "Tuesday", "Wednesday", 
				"Thursday", "Friday", "Saturday")
			)
		# self.setVerticalHeaderLabels(
		# 	list(chain((f"{i} AM" for i in chain((12,), range(1, 12))),
		# 		  (f"{i} PM" for i in chain((12,), range(1, 12)))
		# 		)))
		self.setVerticalHeaderLabels(get_am_pm())
		h = self.horizontalHeader()
		h.setSectionResizeMode(QHeaderView.Stretch)
		h.setMinimumSectionSize(60)
		v = self.verticalHeader()
		v.setSectionResizeMode(QHeaderView.Stretch)
		v.setMinimumSectionSize(20)
		self.setMinimumHeight(300)
		self.setSizePolicy(QSizePolicy.MinimumExpanding, 
			QSizePolicy.MinimumExpanding)
		self.setStyleSheet(" gridline-color: #FFF9F9 ");


	def addCourse(self, user, course):
		user.courses.append(course)
		course_entry = Entry(course['title'], EntryKind.COURSE)
		course_entry.setInfo(course)
		weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
		days = (course[day] for day in weekdays)
		start, end = course['startTime'], course['endTime']
		times = [start, end]
		for i, time in enumerate(times):
			h, m = time.hour, time.minute
			if (m := int(m)) == 0:
				times[i] = int(h)*2
			elif 45 < m < 59:
				times[i] = (int(h)+1)*2
			else:
				times[i] = int(h)*2 - 1

		start, end = times
		# print(f"{start=},{end=},{end-start=}")
		for day_num, in_day in enumerate(days):
			if in_day:
				self.setItem(start+2, day_num+1, course_entry.copy())
				self.setSpan(start+2, day_num+1, end-start, 1)

	# Deprecated function
	def testAdd(self, start, dur, name, days):
		assert not __DEBUG__
		days_bools = list(repeat(False, 5))
		for d in days:
			days_bools[DAYS_MAP[d]] = True
		formatted_args = chain(
			repeat(None, 4), (name, ), repeat(None, 7), 
			days_bools, (None, start, start+dur))
		self.addCourse(*formatted_args)



def stylizeApplication(app):
	app.setStyleSheet(
	" QTabBar::tab" 
	"{"
	" border: none; "
	" font-size: 1 px; "
	" margin-left: 2px; "
	" margin-right: 2px; "
	' margin-bottom: 5px; '
	"}"
	"QTabWidget" 
	"{"
	" background-color: white;"
	"}"
	" QTableWidget {"
	" background-color: white; "
	" }"
	)



user = User()
app = QApplication(sys.argv)
stylizeApplication(app)

login_dialog = Login(user)
login_dialog.getLogin()


x = MainTabs(user)
cal = x.calendar
# user_dict = {
# 	"firstname":None,
# 	"lastname":None,
# 	"studentid":None,
# 	"email": user.email,
# 	"password": user.pw
# }

courses = get_course_information(user.user_dict)
for course in courses:
	cal.addCourse(user, course)
x.fixTabIcons()
x.show()
x.fixTabIcons()
sys.exit(app.exec())
