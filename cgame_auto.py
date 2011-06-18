# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cgame.ui'
#
# Created: Sun Mar 27 15:28:39 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
from PyQt4 import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 350)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 449, 328))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")

        self.frame = QtGui.QFrame(self.gridLayoutWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 111, 21))
        self.label.setObjectName("label")

        self.cmbGameType = QtGui.QComboBox(self.frame)
        self.cmbGameType.setGeometry(QtCore.QRect(150, 0, 281, 24))
        self.cmbGameType.setObjectName("cmbGameType")
        self.cmbGameType.addItem("Categorization Game")
        self.cmbGameType.addItem("Categorization Game with Confidence Rated Belief Updates")
        self.cmbGameType.addItem("Classical Naming Game")

        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.label_3.setObjectName("label_3")

        self.cmbPlot = QtGui.QComboBox(self.frame)
        self.cmbPlot.setGeometry(QtCore.QRect(150, 40, 281, 24))
        self.cmbPlot.setObjectName("cmbPlot")
        self.cmbPlot.addItem("Belief Ratios")
        self.cmbPlot.addItem("No Of Categories")
        self.cmbPlot.addItem("No of Successes vs No Of Fails")
        self.cmbPlot.addItem("Success Rates")

        self.spBNoOfAgents = QtGui.QSpinBox(self.frame)
        self.spBNoOfAgents.setGeometry(QtCore.QRect(150, 120, 271, 23))
        self.spBNoOfAgents.setObjectName("spBNoOfAgents")

        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 86, 131, 20))
        self.label_4.setObjectName("label_4")

        self.cmbBelief = QtGui.QComboBox(self.frame)
        self.cmbBelief.setGeometry(QtCore.QRect(150, 80, 281, 24))
        self.cmbBelief.setObjectName("cmbBelief")
        self.cmbBelief.addItem("None")
        self.cmbBelief.addItem("Logistic Function")
        self.cmbBelief.addItem("tanh Function")

        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(10, 160, 111, 16))
        self.label_5.setObjectName("label_5")

        self.spBDictSize = QtGui.QSpinBox(self.frame)
        self.spBDictSize.setGeometry(QtCore.QRect(150, 160, 271, 23))
        self.spBDictSize.setObjectName("spBDictSize")

        self.chkDraw3D = QtGui.QCheckBox(self.frame)
        self.chkDraw3D.setGeometry(QtCore.QRect(150, 200, 181, 21))
        self.chkDraw3D.setObjectName("chkDraw3D")

        self.btnStart = QtGui.QPushButton(self.frame)
        self.btnStart.setGeometry(QtCore.QRect(150, 270, 85, 27))
        self.btnStart.setObjectName("btnStart")

        self.chkDraw2D = QtGui.QCheckBox(self.frame)
        self.chkDraw2D.setGeometry(QtCore.QRect(150, 230, 181, 21))
        self.chkDraw2D.setObjectName("chkDraw2D")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Game Type:", None, QtGui.QApplication.UnicodeUTF8))

        self.cmbGameType.setItemText(0, QtGui.QApplication.translate("MainWindow", "Categorization Game", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbGameType.setItemText(1, QtGui.QApplication.translate("MainWindow", "Categorization Game with Confidence Rated Belief Updates", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbGameType.setItemText(2, QtGui.QApplication.translate("MainWindow", "Classical Naming Game", None, QtGui.QApplication.UnicodeUTF8))

        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "No Of Agents:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Plot Type:", None, QtGui.QApplication.UnicodeUTF8))

        self.cmbPlot.setItemText(0, QtGui.QApplication.translate("MainWindow", "Belief Ratios", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbPlot.setItemText(1, QtGui.QApplication.translate("MainWindow", "No Of Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbPlot.setItemText(2, QtGui.QApplication.translate("MainWindow", "No Of Successes vs No Of Fails", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbPlot.setItemText(3, QtGui.QApplication.translate("MainWindow", "Success Rates", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Belief Scaling Function:", None, QtGui.QApplication.UnicodeUTF8))
        
        self.cmbBelief.setItemText(0, QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbBelief.setItemText(1, QtGui.QApplication.translate("MainWindow", "Logistic Function", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbBelief.setItemText(2, QtGui.QApplication.translate("MainWindow", "Tanh Function", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Dictionary Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDraw3D.setText(QtGui.QApplication.translate("MainWindow", "Draw 3D Interaction Network", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDraw2D.setText(QtGui.QApplication.translate("MainWindow", "Draw 2D Interaction Network", None, QtGui.QApplication.UnicodeUTF8))
