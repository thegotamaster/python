# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requests_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_requests_window(object):
    def setupUi(self, requests_window):
        requests_window.setObjectName("requests_window")
        requests_window.resize(992, 610)
        self.button_ok = QtWidgets.QPushButton(requests_window)
        self.button_ok.setGeometry(QtCore.QRect(800, 530, 161, 41))
        self.button_ok.setStyleSheet("QPushButton{ background-color:rgb(85, 85, 255); }\n"
"QAbstractButton{ color:rgb(255, 255, 255); font: 10pt \"MS Shell Dlg 2\"; }")
        self.button_ok.setAutoDefault(True)
        self.button_ok.setDefault(False)
        self.button_ok.setFlat(False)
        self.button_ok.setObjectName("button_ok")
        self.date_delivery = QtWidgets.QDateEdit(requests_window)
        self.date_delivery.setGeometry(QtCore.QRect(30, 310, 161, 31))
        self.date_delivery.setToolTipDuration(0)
        self.date_delivery.setStyleSheet("")
        self.date_delivery.setWrapping(False)
        self.date_delivery.setReadOnly(False)
        self.date_delivery.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date_delivery.setObjectName("date_delivery")
        self.date_expiration = QtWidgets.QDateEdit(requests_window)
        self.date_expiration.setGeometry(QtCore.QRect(30, 390, 161, 31))
        self.date_expiration.setToolTipDuration(0)
        self.date_expiration.setStyleSheet("")
        self.date_expiration.setWrapping(False)
        self.date_expiration.setReadOnly(False)
        self.date_expiration.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date_expiration.setObjectName("date_expiration")
        self.text_date_expiration = QtWidgets.QLabel(requests_window)
        self.text_date_expiration.setGeometry(QtCore.QRect(30, 350, 151, 31))
        self.text_date_expiration.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_date_expiration.setObjectName("text_date_expiration")
        self.text_date_delivery = QtWidgets.QLabel(requests_window)
        self.text_date_delivery.setGeometry(QtCore.QRect(30, 270, 151, 31))
        self.text_date_delivery.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_date_delivery.setObjectName("text_date_delivery")
        self.button_menu = QtWidgets.QPushButton(requests_window)
        self.button_menu.setGeometry(QtCore.QRect(30, 40, 161, 41))
        self.button_menu.setStyleSheet("QPushButton{ background-color:rgb(85, 85, 255); }\n"
"QAbstractButton{ color:rgb(255, 255, 255); font: 10pt \"MS Shell Dlg 2\"; }")
        self.button_menu.setAutoDefault(True)
        self.button_menu.setDefault(False)
        self.button_menu.setFlat(False)
        self.button_menu.setObjectName("button_menu")
        self.button_diagram = QtWidgets.QPushButton(requests_window)
        self.button_diagram.setGeometry(QtCore.QRect(30, 150, 161, 41))
        self.button_diagram.setStyleSheet("QPushButton{ background-color: rgb(255, 255, 255); }\n"
"QAbstractButton{ color:rgb(85, 85, 255); font: 11pt \"MS Shell Dlg 2\"; }")
        self.button_diagram.setAutoDefault(True)
        self.button_diagram.setDefault(False)
        self.button_diagram.setFlat(False)
        self.button_diagram.setObjectName("button_diagram")
        self.text_work_requests = QtWidgets.QLabel(requests_window)
        self.text_work_requests.setGeometry(QtCore.QRect(30, 119, 151, 21))
        self.text_work_requests.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_work_requests.setObjectName("text_work_requests")
        self.button_save = QtWidgets.QPushButton(requests_window)
        self.button_save.setGeometry(QtCore.QRect(30, 200, 161, 41))
        self.button_save.setStyleSheet("QPushButton{ background-color: rgb(255, 255, 255); }\n"
"QAbstractButton{ color:rgb(85, 85, 255); font: 11pt \"MS Shell Dlg 2\"; }")
        self.button_save.setAutoDefault(True)
        self.button_save.setDefault(False)
        self.button_save.setFlat(False)
        self.button_save.setObjectName("button_save")
        self.choice_column = QtWidgets.QComboBox(requests_window)
        self.choice_column.setGeometry(QtCore.QRect(580, 530, 161, 31))
        self.choice_column.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_column.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_column.setEditable(False)
        self.choice_column.setCurrentText("")
        self.choice_column.setDuplicatesEnabled(False)
        self.choice_column.setFrame(True)
        self.choice_column.setObjectName("choice_column")
        self.choice_table = QtWidgets.QComboBox(requests_window)
        self.choice_table.setGeometry(QtCore.QRect(320, 530, 161, 31))
        self.choice_table.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_table.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_table.setEditable(False)
        self.choice_table.setCurrentText("")
        self.choice_table.setDuplicatesEnabled(False)
        self.choice_table.setFrame(True)
        self.choice_table.setObjectName("choice_table")
        self.text_table = QtWidgets.QLabel(requests_window)
        self.text_table.setGeometry(QtCore.QRect(240, 530, 71, 31))
        self.text_table.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_table.setObjectName("text_table")
        self.text_column = QtWidgets.QLabel(requests_window)
        self.text_column.setGeometry(QtCore.QRect(500, 530, 71, 31))
        self.text_column.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_column.setObjectName("text_column")
        self.tableWidget = QtWidgets.QTableWidget(requests_window)
        self.tableWidget.setGeometry(QtCore.QRect(240, 30, 721, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(requests_window)
        QtCore.QMetaObject.connectSlotsByName(requests_window)

    def retranslateUi(self, requests_window):
        _translate = QtCore.QCoreApplication.translate
        requests_window.setWindowTitle(_translate("requests_window", "??????????????"))
        self.button_ok.setText(_translate("requests_window", "????"))
        self.text_date_expiration.setText(_translate("requests_window", "???????? ??????????????????"))
        self.text_date_delivery.setText(_translate("requests_window", "???????? ??????????????????????"))
        self.button_menu.setText(_translate("requests_window", "????????"))
        self.button_diagram.setText(_translate("requests_window", "??????????????????"))
        self.text_work_requests.setText(_translate("requests_window", "???????????? ?? ????????????????"))
        self.button_save.setText(_translate("requests_window", "??????????????????"))
        self.text_table.setText(_translate("requests_window", "??????????????"))
        self.text_column.setText(_translate("requests_window", "??????????????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    requests_window = QtWidgets.QDialog()
    ui = Ui_requests_window()
    ui.setupUi(requests_window)
    requests_window.show()
    sys.exit(app.exec_())
