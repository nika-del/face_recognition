import sys
from logging import root

import math
from PIL import Image, ImageDraw, ImageFont

from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont, QIcon
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from qtconsole.qt import QtGui
import face_recognition
from examples.analys import analyser


class Example(QtGui.QWidget):

    def __init__(self):

        super().__init__()
        self.w = None
        self.file = None
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Открыть файл', self)
        btn.setToolTip('Выбрать фото для анализа')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.buttonClicked)
        #btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('FaceAnalyser')
        self.setWindowIcon(QIcon('pin.png'))
        self.show()

    def buttonClicked(self):

        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.file = filename

        self.file = self.file.replace('/', '\\')

        #if not self.file:
        self.w = Widget(self.file)
        # self.w.fileName = self.file
        self.w.show()
        self.close()

        print("F")

        #print(self.w.fileName)


class Widget(QtGui.QWidget):

    def __init__(self, file):

        super().__init__()
        self.fileName = file

        self.setWindowTitle('Analyser')
        self.point = None

        print("klk")
        
        hbox = QVBoxLayout(self)
        pixmap = QPixmap(self.fileName)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)

        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        btn1 = QPushButton("Готово", self)
        hbox.addWidget(btn1)
        btn2 = QPushButton("Очистить", self)
        hbox.addWidget(btn2)

        btn1.clicked.connect(self.button1Clicked)
        btn2.clicked.connect(self.button2Clicked)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def button1Clicked(self):
        newName = "C:\\Users\\Nika Kim\\Desktop\\faces\\12345.png"
        print("klkkluyhoiudy")
        self.lbl.pixmap().save(newName, 'png')

        an = analyser()

        an.analys(newName)

        print("sdfghjkl")
        self.close()

    def button2Clicked(self):
        pixmap = QPixmap(self.fileName)
        self.lbl.setPixmap(pixmap)


    def mousePressEvent(self, event):

        self.point = event.pos()

        # Вызов перерисовки виджета
        self.update()


    def mouseReleaseEvent(self, event):

        self.point = None


    def paintEvent(self, event):

        super().paintEvent(event)

        # Если нет
        if not self.point:
            return

        painter = QPainter(self.lbl.pixmap())
        painter.setPen(QPen(Qt.red, 10.0))
        painter.drawPoint(self.point)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()


    sys.exit(app.exec_())








