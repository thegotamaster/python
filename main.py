import ftplib
import sys
import psycopg2
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton

import add_note_window
import auth_window
import change_note_window
import menu_window
import open_compound_form_window
import requests_window
import tables_window

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication

# подключение к базе данных
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)

# создаем курсор
cursor = conn.cursor()


# форма авторизации
class Ui_auth_form(QtWidgets.QDialog, auth_window.Ui_auth_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_enter.clicked.connect(self.MenuWindow)
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()

    # проверка на ввод данных (авторизация)
    def auth(self):
        if self.login == "" and self.password == "":
            conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                    port=5432)
            cursor = conn.cursor()
            return cursor, conn
        else:
            return 0

    # соединение с формой меню
    def MenuWindow(self):
        x = Ui_menu_form(conn, cursor)
        x.exec_()


# форма меню
class Ui_menu_form(QtWidgets.QDialog, menu_window.Ui_menu_form):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_tables.clicked.connect(self.TablesWindow)
        self.button_requests.clicked.connect(self.RequestsWindow)
        self.button_exit.clicked.connect(QCoreApplication.instance().quit)

    # соединение с формой таблиц
    def TablesWindow(self):
        x = Ui_tables_window(conn, cursor)
        x.exec_()

    # соединение с формой запросов
    def RequestsWindow(self):
        x = Ui_requests_window(conn, cursor)
        x.exec_()


# форма таблиц
class Ui_tables_window(QtWidgets.QDialog, tables_window.Ui_tables_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_menu.clicked.connect(self.MenuWindow)
        self.button_add.clicked.connect(self.AddWindow)
        self.button_change.clicked.connect(self.ChangeWindow)
        self.button_open.clicked.connect(self.CompoundWindow)
        self.button_all.clicked.connect(self.All)
        self.button_generate.clicked.connect(self.Generate)
        self.button_search.clicked.connect(self.Search)
        self.button_delete.clicked.connect(self.Delete)

        self.components()

    # компоненты комбобоксов
    def components(self):
        self.choice_table.addItem("Каталог", ["Название лекарства"])
        self.choice_table.addItem("Лекарства", ["Штрих-код", "Инструкция"])
        self.choice_table.addItem("Партия", ["Номер партии", "Количество упаковок", "Цена(партия)", "Цена(аптека)",
                                             "Дата выпуска", "Дата окончания", "Дата поступления", "Наличие дефекта"])
        self.choice_table.addItem("Аптеки", ["Название аптеки", "Номер аптеки", "Адрес", "Телефон"])
        self.choice_table.activated.connect(self.clicker)

        self.button = QPushButton("Вывести", self)
        self.button.setGeometry(390, 610, 90, 30)
        self.button.setStyleSheet("QPushButton{ background-color:rgb(85, 85, 255); }\n"
                                  "QAbstractButton{ color:rgb(255, 255, 255); font: 8pt \"MS Shell Dlg 2\"; }")
        print(self.choice_table.count())
        self.button.pressed.connect(self.changer)

    # кейсы комбобоксов
    def changer(self):
        match self.choice_column.currentText():
            case "Название лекарства":
                self.widget_catalog()
            case "Штрих-код":
                self.widget_medicine1()
            case "Инструкция":
                self.widget_medicine2()
            case "Номер партии":
                self.widget_party1()
            case "Количество упаковок":
                self.widget_party2()
            case "Цена(партия)":
                self.widget_party3()
            case "Ценв(аптека)":
                self.widget_party4()
            case "Дата выпуска":
                self.widget_party5()
            case "Дата окончания":
                self.widget_party6()
            case "Дата поступления":
                self.widget_party7()
            case "Наличие дефекта":
                self.widget_party8()
            case "Название аптеки":
                self.widget_pharmacy1()
            case "Номер аптеки":
                self.widget_pharmacy2()
            case "Адрес":
                self.widget_pharmacy3()
            case "Телефон":
                self.widget_pharmacy4()

    # взаимосвязь двух комбобоксов
    def clicker(self, index):
        self.choice_column.clear()
        self.choice_column.addItems(self.choice_table.itemData(index))

    # виджет таблицы "Каталог" по полю "Имя"
    def widget_catalog(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select name, catalog.name_key from catalog")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(1)
        labels = ['Название лекарства']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Лекарства" по полю "Штрих-код"
    def widget_medicine1(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select name_key, shape_key, group_key, manufacturer_key, barcode, medicine.medicine_key, medicine.name_key, medicine.group_key, medicine.manufacturer_key from medicine")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(5)
        labels = ['Название лекарства', 'Форма выпуска', 'Фармакологическая группа', 'Фирма производитель', 'Штрих-код']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Лекарства" по полю "Инструкция"
    def widget_medicine2(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select name_key, shape_key, group_key, manufacturer_key, comments, medicine.medicine_key from medicine")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(5)
        labels = ['Название лекарства', 'Форма выпуска', 'Фармакологическая группа', 'Фирма производитель',
                  'Инструкция']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Номер партии"
    def widget_party1(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select numberparty, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Номер партии', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Количество упаковок"
    def widget_party2(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select count, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Количество упаковок', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Цена(партия)"
    def widget_party3(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select price, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Цена(партия)', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Цена(аптека)"
    def widget_party4(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select pricepharm, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Цена(аптека)', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Дата выпуска"
    def widget_party5(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select datestart, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Дата выпуска', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Дата окончания"
    def widget_party6(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select datefinish, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Дата окончания', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Дата поступления"
    def widget_party7(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select datefact, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Дата поступления', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Партия" по полю "Наличие дефекта"
    def widget_party8(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select defect, mark_key, employee_key, party.party_key from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Наличие дефекта', 'Причина возврата', 'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Аптека" по полю "Название аптеки"
    def widget_pharmacy1(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select pharmacy, type_key, district_key, pharmacy.pharmacy_key from pharmacy")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Название аптеки', 'Тип собственности', 'Район города']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Аптека" по полю "Номер аптеки"
    def widget_pharmacy2(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select number, type_key, district_key, pharmacy.pharmacy_key from pharmacy")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Номер аптеки', 'Тип собственности', 'Район города']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Аптека" по полю "Адрес"
    def widget_pharmacy3(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select addresspharm, type_key, district_key, pharmacy.pharmacy_key from pharmacy")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Адрес', 'Тип собственности', 'Район города']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет таблицы "Аптека" по полю "Телефон"
    def widget_pharmacy4(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select phone, type_key, district_key, pharmacy.pharmacy_key from pharmacy")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(3)
        labels = ['Телефон', 'Тип собственности', 'Район города']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # соединение с меню
    def MenuWindow(self):
        x = Ui_menu_form(conn, cursor)
        x.exec_()

    # соединение с формой добавить запись
    def AddWindow(self):
        x = Ui_add_note_window(conn, cursor)
        x.exec_()

    # соединение с формой редактировать запись
    def ChangeWindow(self):
        x = Ui_change_note_window(conn, cursor)
        x.exec_()

    # соединение с составной формой
    def CompoundWindow(self):
        x = Ui_open_compound_form_window(conn, cursor)
        x.exec_()

    # кнопка "Все записи"
    def All(self):
        pass

    # кнопка "Генерация"
    def Generate(self):
        pass

    # кнопка "Поиск"
    def Search(self):
        pass

    # кнопка "Удалить"
    def Delete(self):
        pass


# форма запросов
class Ui_requests_window(QtWidgets.QDialog, requests_window.Ui_requests_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_menu.clicked.connect(self.MenuWindow)
        self.button_ok.clicked.connect(self.Ok)
        self.button_diagram.clicked.connect(self.Diagram)
        self.button_save.clicked.connect(self.Save)

    # соединение с формой меню
    def MenuWindow(self):
        x = Ui_menu_form(conn, cursor)
        x.exec_()

    # кнопка "Ок"
    def Ok(self):
        pass

    # кнопка "Диаграмма"
    def Diagram(self):
        pass

    # кнопка "Сохранить"
    def Save(self):
        pass


# форма добавить запись
class Ui_add_note_window(QtWidgets.QDialog, add_note_window.Ui_add_note_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_save.clicked.connect(self.save_note)

    # кнопка "Сохранить"
    def save_note(self):
        if not self.path == "" and not self.choice_maker.curentText() == "" and not self.choice_name.currentText() == "" and not self.choice_release.currentText() == "" and not self.choice_pharmacology.currentText() == "" and not self.instruction_memo.toPlainText() == "" and not self.barcode.toPlainText():
            self.cursor.execute(
                f"select manufacturer_key from manufacturer where manufacturer={self.choice_maker.currentText()}")
            manufacturer = self.cursor.fetchall()[0][0]
            self.cursor.execute(f"select name_key from catalogue where name={self.choice_name.currentText()}")
            name = self.cursor.fetchall()[0][0]
            self.cursor.execute(f"select shape_key from shape where shape={self.choice_release.currentText()}")
            shape = self.cursor.fetchall()[0][0]
            self.cursor.execute(f"select group_key from group where group={self.choice_pharmacology.currentText()}")
            group = self.cursor.fetchall()[0][0]
            self.path = self.path[0].split('/')[-1]
            self.cursor.execute(
                f"insert into general(manufacturer_key_internal,name_key_internal, shape_key_internal, "
                f"group_key_internal, instruction_memo, barcode) values ({manufacturer},{name},{shape},{group},"
                f"{self.instruction_memo.toPlainText()},{self.barcode.toPlainText()})")

            ftp = ftplib.FTP("localhost")
            ftp.login("ftp", "ftp")
            ftp_upload(ftp, self.path)
            ftp.quit()
            pass
        else:
            pass


# форма редактировать запись
class Ui_change_note_window(QtWidgets.QDialog, change_note_window.Ui_change_note_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_save.clicked.connect(self.save_note)

    # кнопка "Сохранить"
    def save_note(self):
        pass


# составная форма
class Ui_open_compound_form_window(QtWidgets.QDialog, open_compound_form_window.Ui_open_compound_form_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_ok.clicked.connect(self.Ok)

    # кнопка "Ок"
    def Ok(self):
        pass


# проверка подключения к базе данных
if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")

# функция main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_auth_form()
    window.show()
    sys.exit(app.exec_())
