# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_compound_form_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_open_compound_form_window(object):
    def setupUi(self, open_compound_form_window):
        open_compound_form_window.setObjectName("open_compound_form_window")
        open_compound_form_window.resize(1020, 615)
        self.button_ok = QtWidgets.QPushButton(open_compound_form_window)
        self.button_ok.setGeometry(QtCore.QRect(810, 530, 161, 41))
        self.button_ok.setStyleSheet("QPushButton{ background-color:rgb(85, 85, 255); }\n"
"QAbstractButton{ color:rgb(255, 255, 255); font: 10pt \"MS Shell Dlg 2\"; }")
        self.button_ok.setAutoDefault(True)
        self.button_ok.setDefault(False)
        self.button_ok.setFlat(False)
        self.button_ok.setObjectName("button_ok")
        self.date_delivery = QtWidgets.QDateEdit(open_compound_form_window)
        self.date_delivery.setGeometry(QtCore.QRect(40, 380, 141, 31))
        self.date_delivery.setToolTipDuration(0)
        self.date_delivery.setStyleSheet("")
        self.date_delivery.setWrapping(False)
        self.date_delivery.setReadOnly(False)
        self.date_delivery.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date_delivery.setObjectName("date_delivery")
        self.text_date_delivery = QtWidgets.QLabel(open_compound_form_window)
        self.text_date_delivery.setGeometry(QtCore.QRect(40, 340, 151, 31))
        self.text_date_delivery.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_date_delivery.setObjectName("text_date_delivery")
        self.date_expiration = QtWidgets.QDateEdit(open_compound_form_window)
        self.date_expiration.setGeometry(QtCore.QRect(260, 380, 141, 31))
        self.date_expiration.setToolTipDuration(0)
        self.date_expiration.setStyleSheet("")
        self.date_expiration.setWrapping(False)
        self.date_expiration.setReadOnly(False)
        self.date_expiration.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.date_expiration.setObjectName("date_expiration")
        self.text_date_expiration = QtWidgets.QLabel(open_compound_form_window)
        self.text_date_expiration.setGeometry(QtCore.QRect(260, 340, 151, 31))
        self.text_date_expiration.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_date_expiration.setObjectName("text_date_expiration")
        self.text_pharmacy = QtWidgets.QLabel(open_compound_form_window)
        self.text_pharmacy.setGeometry(QtCore.QRect(40, 30, 121, 31))
        self.text_pharmacy.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_pharmacy.setObjectName("text_pharmacy")
        self.choice_pharmacy = QtWidgets.QComboBox(open_compound_form_window)
        self.choice_pharmacy.setGeometry(QtCore.QRect(40, 60, 361, 31))
        self.choice_pharmacy.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_pharmacy.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_pharmacy.setEditable(False)
        self.choice_pharmacy.setCurrentText("")
        self.choice_pharmacy.setDuplicatesEnabled(False)
        self.choice_pharmacy.setFrame(True)
        self.choice_pharmacy.setObjectName("choice_pharmacy")
        self.choice_district = QtWidgets.QComboBox(open_compound_form_window)
        self.choice_district.setGeometry(QtCore.QRect(40, 200, 361, 31))
        self.choice_district.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_district.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_district.setEditable(False)
        self.choice_district.setCurrentText("")
        self.choice_district.setDuplicatesEnabled(False)
        self.choice_district.setFrame(True)
        self.choice_district.setObjectName("choice_district")
        self.text_district = QtWidgets.QLabel(open_compound_form_window)
        self.text_district.setGeometry(QtCore.QRect(40, 170, 121, 31))
        self.text_district.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_district.setObjectName("text_district")
        self.choice_number = QtWidgets.QComboBox(open_compound_form_window)
        self.choice_number.setGeometry(QtCore.QRect(40, 130, 361, 31))
        self.choice_number.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_number.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_number.setEditable(False)
        self.choice_number.setCurrentText("")
        self.choice_number.setDuplicatesEnabled(False)
        self.choice_number.setFrame(True)
        self.choice_number.setObjectName("choice_number")
        self.choice_address = QtWidgets.QComboBox(open_compound_form_window)
        self.choice_address.setGeometry(QtCore.QRect(40, 270, 361, 31))
        self.choice_address.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.choice_address.setStyleSheet("QLineEdit{ font: 10pt \"MS Shell Dlg 2\"; }")
        self.choice_address.setEditable(False)
        self.choice_address.setCurrentText("")
        self.choice_address.setDuplicatesEnabled(False)
        self.choice_address.setFrame(True)
        self.choice_address.setObjectName("choice_address")
        self.text_address = QtWidgets.QLabel(open_compound_form_window)
        self.text_address.setGeometry(QtCore.QRect(40, 240, 221, 31))
        self.text_address.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_address.setObjectName("text_address")
        self.text_number = QtWidgets.QLabel(open_compound_form_window)
        self.text_number.setGeometry(QtCore.QRect(40, 100, 121, 31))
        self.text_number.setStyleSheet("QLabel{ color:rgb(111, 111, 111); font: 10pt \"MS Shell Dlg 2\"; }\n"
"")
        self.text_number.setObjectName("text_number")
        self.tableWidget = QtWidgets.QTableWidget(open_compound_form_window)
        self.tableWidget.setGeometry(QtCore.QRect(450, 30, 521, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(open_compound_form_window)
        QtCore.QMetaObject.connectSlotsByName(open_compound_form_window)

    def retranslateUi(self, open_compound_form_window):
        _translate = QtCore.QCoreApplication.translate
        open_compound_form_window.setWindowTitle(_translate("open_compound_form_window", "Составная форма"))
        self.button_ok.setText(_translate("open_compound_form_window", "Ок"))
        self.text_date_delivery.setText(_translate("open_compound_form_window", "Дата поступления"))
        self.text_date_expiration.setText(_translate("open_compound_form_window", "Дата окончания"))
        self.text_pharmacy.setText(_translate("open_compound_form_window", "Аптека"))
        self.text_district.setText(_translate("open_compound_form_window", "Район города"))
        self.text_address.setText(_translate("open_compound_form_window", "Адрес"))
        self.text_number.setText(_translate("open_compound_form_window", "Номер аптеки"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    open_compound_form_window = QtWidgets.QDialog()
    ui = Ui_open_compound_form_window()
    ui.setupUi(open_compound_form_window)
    open_compound_form_window.show()
    sys.exit(app.exec_())