import sys
from os import path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from dbController import dbController



class calendarFrame():


    def __init__(self, email):
        self.mainWidget = QWidget()
        self.controller = dbController()
        self.regClassList = self.controller.getRegisteredClasses(email)
        self.examsList = self.controller.get_user_exams(email)
        self.assignmentsList = self.controller.get_user_assignments(email)
        self.classExamDict = {}
        for course in self.regClassList:
            string = course[1] + " " + str(course[3])
            self.classExamDict[course[5]] = string
        

    class examListItem(QListWidgetItem):
        def __init__(self, exam, calendarFrame, parent = None):
            QListWidgetItem.__init__(self, parent)
            if exam[4] != None:
                self.date = exam[4]
                self.day = self.date.day
                self.month = self.date.month

                match self.month:
                    case 1:
                        monthString = "\nJAN" + "  " + str(self.day)
                    case 2:
                        monthString = "\nFEB"  + "  " + str(self.day)
                    case 3:
                        monthString = "\nMAR" + "  " + str(self.day)
                    case 4:
                        monthString = "\nAPR" + "  " + str(self.day)
                    case 5:
                        monthString = "\nMAY" + "  " + str(self.day)
                    case 6:
                        monthString = "\nJUN" + "  " + str(self.day)
                    case 7:
                        monthString = "\nJUL" + "  " + str(self.day)
                    case 8:
                        monthString = "\nAUG" + "  " + str(self.day)
                    case 9:
                        monthString = "\nSEP" + "  " + str(self.day)
                    case 10:
                        monthString = "\nOCT" + "  " + str(self.day)
                    case 11:
                        monthString = "\nNOV" + "  " + str(self.day)
                    case 12:
                        monthString = "\nDEC" + "  " + str(self.day)
            else:
                monthString = ""
                self.date = None


            #print(self.date)
            self.setSizeHint(QSize(500, 100))
            self.setBackground(QColor(128,128,128,100))
            text = calendarFrame.classExamDict[exam[8]] + " " + exam[3] + monthString
            self.setText(text)
            self.setTextAlignment(Qt.AlignJustify)
            

    class calendar(QCalendarWidget):
        def __init__(self, calendarFrame, parent = None):
            super().__init__(parent)
            self.calendarFrame = calendarFrame
            
        # def paintCell(self, painter, rect, date):
        #     super().paintCell(painter, rect,date)
        #     for exam in self.calendarFrame.assignmentsList:
        #         #print(exam[4])
        #         #qdate = QDate.fromString(exam[4])
        #         if date in qdate:
        #             painter.setBrush(Qt.red)
        #             painter.drawEllipse(rect.topLeft() + QPoint(12,7),3,3)



    def getWidget(self):
        self.layout = QHBoxLayout()
        self.list = QListWidget()
        self.list.setItemAlignment(Qt.AlignJustify)
        self.list.setStyleSheet("QListWidget"
                                  "{"
                                  "border : 2px solid black;"
                                  "}"
                                  "QListView::item"
                                  "{"
                                  "border : 2px solid black;"
                                  "background: #9ea2a2"
                                  "}"
                                  "QListView::item:selected"
                                  "{"
                                  "background : #2475dd;"
                                  "}")
        font = QFont()
        font.setPointSize(20)
        self.list.setFont(font)
        self.list.setWordWrap(True)
        # self.list.setMinimumWidth(100)
        # self.list.setSizePolicy(
        #     QSizePolicy.Minimum,QSizePolicy.Expanding
        # )
        for exam in self.examsList:
            self.list.addItem(self.examListItem(exam, self))
        self.cal = self.calendar(self)
        self.cal.setGridVisible(True)
        
        self.list.setMaximumWidth(500)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.cal)
        self.mainWidget.setLayout(self.layout)
        return self.mainWidget



if __name__ == "__main__":
    app = QApplication(sys.argv)
    calendarF = calendarFrame("nicholas.corneau@mail.mcgill.ca")
    widget = calendarF.getWidget()
    widget.show()
    # yourWidget = yourConstructor(yourArgs)
    sys.exit(app.exec())
