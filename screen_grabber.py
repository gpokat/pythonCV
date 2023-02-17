import numpy as np
from PIL import Image, ImageGrab

import pygetwindow as gw
from mss import mss
import cv2

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

import sys


class MForm(QDialog):
    def __init__(self, parent=None):
        super(MForm, self).__init__(parent)
        
        self.selected_window = ""
 
        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.SingleSelection)

        def onChange():
            self.selected_window = self.listwidget.currentItem().text()
            print([self.selected_window])

        def onOkClicked():
            #self.listwidget.clear() #TODO
            print([self.selected_window])
            if len(self.selected_window) != 0:
                sct = mss()
                while True:
                    hwnd = gw.getWindowsWithTitle(self.selected_window)[0] #TODO with name
                    rect = {"top": hwnd.top, "left": hwnd.left, "width": hwnd.width, "height": hwnd.height}
                    img = Image.frombytes('RGB', (hwnd.width, hwnd.height), sct.grab(rect).rgb)
                    cv2.imshow('TestAI', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

        self.listwidget.itemSelectionChanged.connect(onChange)

        atitles = gw.getAllTitles()
        for i in range(len(atitles)):
            if len(atitles[i]) != 0:
                self.listwidget.addItem(atitles[i])

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.listwidget, 1)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(onOkClicked)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(okBtn)

        #listwidget.show()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Test1AI")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MForm()
    sys.exit(app.exec_())