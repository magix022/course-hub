from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel, QComboBox, QListWidget, QMenu, QListWidgetItem, QVBoxLayout
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize, QEvent
import sys
from itertools import chain, repeat
from enum import IntEnum
from os import path



class TasksView(QWidget):
	def __init__(self, master=None):
		QWidget.__init__(self, master)
		self.layout = QHBoxLayout()
		leftLayout = QVBoxLayout()
		rightLayout = QVBoxLayout()
		leftLabel = QLabel("Pending tasks")
		leftLayout.addWidget(leftLabel)
		rightLabel = QLabel("To-do")
		rightLayout.addWidget(rightLabel)
		self.tasksList = QListWidget()
		self.newList = NewList(self.tasksList)
		leftLayout.addWidget(self.newList)
		rightLayout.addWidget(self.tasksList)
		self.layout.addLayout(leftLayout)
		self.layout.addLayout(rightLayout)
		self.setLayout(self.layout)

	def getLayout(self):
		return self.layout

	def addTask(self, event):
		item = NewTask(event)
		self.addItem(item)


class NewList(QListWidget):
	def __init__(self, other_list, master=None):
		QListWidget.__init__(self, master)
		self.other_list = other_list

	def itemRightClicked(self, item, _):
		menu = QMenu()
		add = menu.addAction(f'Add task')
		action = menu.addSeparator()
		ignore = menu.addAction(f'Ignore')

		add.clicked.connect(lambda *_: self.moveTask(item))
		ignore.clicked.connect(lambda *_: self.ignoreTask(item))
		
		# _ = menu.addAction(f'SIZE: {chunk.size} ({chunk.size_val})')
		
		# action1 = menu.addAction('whatsup')
		menu.exec_(pt)

	def moveTask(self, item):
		item = self.takeItem(self.row(item))
		other_list.addItem(item)

	def ignoreTask(self, item):
		_ = self.takeItem(self.row(item))


class NewTask(QListWidgetItem):
	def __init__(self, event):
		type_ = event['''type''']
		time_str = event['deadline'].strftime("%d/%m/%y")
		display = f'{type_}: Due {time_str}'
		QListWidgetItem.__init__(self,display)
		self.data = event




"""

[{'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 23, 0, 0), 
'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c1a38b0>}, 
{'type': 'webwork quiz', 'deadline': None, 'length': 0, 'title': 'Quiz 1', 
'date': <generator object DateFinder.find_dates at 0x10c1a3ed0>}, 
{'type': 'final quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680190>}, {'type': 'quiz', 'deadline': None, 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680200>}, {'type': 'final quiz', 'deadline': datetime.datetime(2022, 1, 23, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680270>}, {'type': 'webwork quiz', 'deadline': None, 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680040>}, {'type': 'final quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c6802e0>}, {'type': 'quiz', 'deadline': None, 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c6803c0>}, {'type': 'final quiz', 'deadline': datetime.datetime(2022, 1, 23, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680430>}, {'type': 'webwork quiz', 'deadline': datetime.datetime(2022, 1, 2, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680350>}, {'type': 'final quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680510>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 2, 3, 0, 0), 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680580>}, {'type': 'final', 'deadline': None, 'length': 0, 'title': 'Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c6806d0>}, {'type': 'exam midterm', 'deadline': datetime.datetime(2022, 2, 22, 0, 0), 'length': 0, 'title': 'Midterm date', 'date': <generator object DateFinder.find_dates at 0x10c6805f0>}, {'type': 'exam midterm', 'deadline': datetime.datetime(2022, 2, 22, 0, 0), 'length': 0, 'title': 'Midterm date', 'date': <generator object DateFinder.find_dates at 0x10c680120>}, {'type': 'exam midterm', 'deadline': datetime.datetime(2022, 2, 22, 0, 0), 'length': 0, 'title': 'Midterm date', 'date': <generator object DateFinder.find_dates at 0x10c6804a0>}, {'type': 'exam', 'deadline': datetime.datetime(2022, 2, 22, 0, 0), 'length': 0, 'title': 'Midterm date', 'date': <generator object DateFinder.find_dates at 0x10c680740>}, {'type': 'exam', 'deadline': None, 'length': 0, 'title': 'Tutorial details and TA office hours', 'date': <generator object DateFinder.find_dates at 0x10c680890>}, {'type': 'exam', 'deadline': None, 'length': 0, 'title': 'Tutorial details and TA office hours', 'date': <generator object DateFinder.find_dates at 0x10c680820>}, {'type': 'exam', 'deadline': None, 'length': 0, 'title': 'Tutorial details and TA office hours', 'date': <generator object DateFinder.find_dates at 0x10c680900>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 2, 0, 0), 'length': 0, 'title': 'Quiz 2 Released', 'date': <generator object DateFinder.find_dates at 0x10c680660>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 2, 0, 0), 'length': 0, 'title': 'Quiz 2 Released', 'date': <generator object DateFinder.find_dates at 0x10c6807b0>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 2, 0, 0), 'length': 0, 'title': 'Quiz 2 Released', 'date': <generator object DateFinder.find_dates at 0x10c680ba0>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1 Grades Released', 'date': <generator object DateFinder.find_dates at 0x10c680c80>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1 Grades Released', 'date': <generator object DateFinder.find_dates at 0x10c680cf0>}, {'type': 'quiz', 'deadline': datetime.datetime(2022, 1, 1, 0, 0), 'length': 0, 'title': 'Quiz 1 Grades Released', 'date': <generator object DateFinder.find_dates at 0x10c6809e0>}, {'type': 'assignment', 'deadline': None, 'length': 0, 'title': 'Assignment 1 Posted', 'date': <generator object DateFinder.find_dates at 0x10c680d60>}, {'type': 'assignment', 'deadline': None, 'length': 0, 'title': 'Assignment 1 Posted', 'date': <generator object DateFinder.find_dates at 0x10c680dd0>}, {'type': 'assignment', 'deadline': None, 'length': 0, 'title': 'Assignment 1 Posted', 'date': <generator object DateFinder.find_dates at 0x10c680c10>}, {'type': 'quiz', 'deadline': None, 'length': 0, 'title': 'Lecture 2 Slides and Notes, Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680b30>}, {'type': 'quiz', 'deadline': None, 'length': 0, 'title': 'Lecture 2 Slides and Notes, Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680ac0>}, {'type': 'quiz', 'deadline': None, 'length': 0, 'title': 'Lecture 2 Slides and Notes, Quiz 1', 'date': <generator object DateFinder.find_dates at 0x10c680f90>}]
"""

"""
Event: type, deadline (datetime), length = 0, raw_announcement(
		title, date, text
	)
"""