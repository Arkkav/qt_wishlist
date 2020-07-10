# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/arkkav/projects/qt_wishlist/wishlist.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 498)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QPushButton(self.centralwidget)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnEdit.setObjectName("btnEdit")
        self.horizontalLayout.addWidget(self.btnEdit)
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnAdd.setText(_translate("MainWindow", "Create"))
        self.btnEdit.setText(_translate("MainWindow", "Edit"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
