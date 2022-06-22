import ftplib
import multiprocessing
import random
import string
import sys
import datetime
import time
import xlsxwriter
import numpy as np

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
            case "Цена(аптека)":
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
        cursor.execute(
            f"Select name_key, shape_key, group_key, manufacturer_key, barcode, medicine.medicine_key, medicine.name_key, medicine.group_key, medicine.manufacturer_key from medicine")
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
        cursor.execute(
            f"Select name_key, shape_key, group_key, manufacturer_key, comments, medicine.medicine_key from medicine")
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
        match self.choice_table.currentText():
            case "Каталог":
                self.widget_catalog11()
            case "Лекарства":
                self.widget_medicine11()
            case "Партия":
                self.widget_party11()
            case "Аптеки":
                self.widget_pharmacy11()

    # виджет для всех записей каталога
    def widget_catalog11(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from catalog")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(2)
        labels = ['Номер лекарства', 'Название лекарства']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет для всех записей лекарств
    def widget_medicine11(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from medicine")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(6)
        labels = ['Название лекарства', 'Форма выпуска', 'Фармакологическая группа', 'Фирма производитель', 'Штрих-код',
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

    # виджет для всех записей партии
    def widget_party11(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from party")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(10)
        labels = ['Номер партии', 'Название лекарства', 'Количество упаковок', 'Цена(партия)', 'Цена(аптека)',
                  'Дата выпуска', 'Дата окончания', 'Дата поступления', 'Наличие дефекта', 'Причина возврата',
                  'Сотрудник']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # виджет для всех записей аптек
    def widget_pharmacy11(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from pharmacy")
        conn.commit()
        self.tableWidget_tables.clear()
        rows = cursor.fetchall()
        self.tableWidget_tables.setRowCount(len(rows))
        self.tableWidget_tables.setColumnCount(6)
        labels = ['Название аптеки', 'Номер аптеки', 'Тип собственности', 'Район города', 'Адрес', 'Телефон']
        self.tableWidget_tables.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget_tables.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget_tables.resizeColumnsToContents()

    # дополнительная функция для многопотока
    def loop_pool(self, catalog, medicine, party, pharmacy, employee, manufacturer, name_range, shape_range,
                  group_range, manufacturers_range, instruction_photo, defect_range, mark_range, employees_range,
                  pharmacies_range, type_range, district_range, address_range, country_range, letters, domains,
                  gen_range):
        for i in range(0, gen_range):
            catalog += f"(1,'{random.choice(name_range)}'),"
            medicine += f"({random.choice(name_range)},{random.choice(shape_range)}, {random.choice(group_range)}, {random.choice(manufacturers_range)}, '{random.randint(1000000000, 9999999999)}', '{random.choice(instruction_photo)}'),"
            party += f"('{random.randint(1, 10000)}',{random.choice(name_range)}, '{random.randint(1, 10000)}', '{random.uniform(100.00, 200.00)}', '{random.uniform(300.00, 400.00)}', '{datetime.date(np.random.randint(2013, datetime.datetime.now().year - 1), np.random.randint(1, 12), np.random.randint(1, 28))}', '{datetime.date(np.random.randint(2015, datetime.datetime.now().year - 1), np.random.randint(1, 12), np.random.randint(1, 28))}','{datetime.date(np.random.randint(2013, datetime.datetime.now().year - 1), np.random.randint(1, 12), np.random.randint(1, 28))}','{random.choice(defect_range)}', {random.choice(mark_range)}, {random.choice(employees_range)}),"
            pharmacy += f"('{random.choice(pharmacies_range)}', '{random.randint(1, 10000)}', {random.choice(type_range)}, {random.choice(district_range)}, '{random.choice(address_range)}, {random.randint(1, 100)}', '{random.randint(1000000000, 9999999999)}'),"
            employee += f"('{random.choice(employees_range)}', {random.choice(pharmacies_range)}),"
            manufacturer += f"('{random.choice(manufacturers_range)}', {random.choice(country_range)}, '{random.choice(letters)}, {random.choice(domains)}', '{random.randint(1900, int(datetime.datetime.now().year - 1))}'),"
        return np.array([catalog, medicine, party, pharmacy, employee, manufacturer])

    # кнопка "Генерация"
    def Generate(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        gen_range = 10000
        cursor.execute(
            "TRUNCATE country, district, employee, grouppharm, mark, shape, type, catalog RESTART IDENTITY CASCADE")
        conn.commit()

        name = ["Фенитоин", "Тримипрамин", "Пирацетам", "Спазмалгон", "Медиана", "Стрептомицин"]
        name_range = range(1, len(name))
        request = ",".join("('%s')" % x for x in name)
        cursor.execute("INSERT INTO catalog(name) VALUES " + request)
        conn.commit()

        pharmacies = ["Производство медикаментов", "Канонфарма продакшн", "Реплек фарм", "Балканфарма", "Гедеон рихтер",
                      "Синтез"]
        pharmacies_range = range(1, len(pharmacies))
        request = ",".join("('%s')" % x for x in pharmacies)
        cursor.execute("INSERT INTO pharmacy(pharmacy) VALUES " + request)
        conn.commit()

        country = ["Россия", "Беларусь", "Германия", "Чехия", "Южная Корея", "Италия", "Словакия", "Португалия",
                   "Болгария", "Молдова"]
        country_range = range(1, len(country))
        request = ",".join("('%s')" % x for x in country)
        cursor.execute("INSERT INTO country(country) VALUES " + request)
        conn.commit()

        district = ["Куйбышевский", "Калининский", "Ворошиловский", "Будённовский", "Киевский", "Кировский",
                    "Ленинский", "Пролетарский", "Петровский"]
        district_range = range(1, len(district))
        request = ",".join("('%s')" % x for x in district)
        cursor.execute("INSERT INTO district(district) VALUES " + request)
        conn.commit()

        address = ["улица Западная", "улица Восточная", "улица Южная", "улица Северная", "улица Юго-Западная",
                   "улица Юго-Восточная", "улица Северо-Западная", "улица Северо-Восточная"]
        #Вот этот массив сразу передаешь в луп пул и в нём добавляешь В САМЫЙ КОНЕЦ RANDOM.CHOICE.

        employees = ["Безуглый В.В.", "Золотовский М.В.", "Зинатулин А.В."]
        employees_range = range(1, len(employees))
        request = ",".join("('%s')" % x for x in employees)
        cursor.execute("INSERT INTO employee(employee) VALUES " + request)
        conn.commit()

        group = ["Противоэпилептическое средство", "Антидепрессант", "Ноотропное средство",
                 "Обезбаливающее средство", "Гормональное средство", "Антибиотик"]
        group_range = range(1, len(group))
        request = ",".join("('%s')" % x for x in group)
        cursor.execute("INSERT INTO grouppharm(group) VALUES " + request)
        conn.commit()

        shape = ["Таблетка", "Капсула", "Порошок", "Мазь", "Сироп", "Пиллюля"]
        shape_range = range(1, len(shape))
        request = ",".join("('%s')" % x for x in shape)
        cursor.execute("INSERT INTO shape(shape) VALUES " + request)
        conn.commit()

        type = ["Частная", "Общая", "Государственная"]
        type_range = range(1, len(type))
        request = ",".join("('%s')" % x for x in type)
        cursor.execute("INSERT INTO type(type) VALUES " + request)
        conn.commit()

        manufacturers = ["Производство медикаментов", "Канонфарма продакшн", "Реплек фарм", "Балканфарма",
                         "Гедеон рихтер", "Синтез"]
        manufacturers_range = range(1, len(manufacturers))
        request = ",".join("('%s')" % x for x in manufacturers)
        cursor.execute("INSERT INTO manufacturer(manufacturer) VALUES " + request)
        conn.commit()

        defect = ["Да", "Нет"]
        defect_range = range(1, len(defect))
        request = ",".join("('%s')" % x for x in defect)
        cursor.execute("INSERT INTO defect(defect) VALUES " + request)
        conn.commit()

        if defect == 0:
            mark = ["Испорчена упаковка", "Просрочен", "Не хватает медикаментов"]
            mark_range = range(1, len(mark))
            request = ",".join("('%s')" % x for x in mark)
            cursor.execute("INSERT INTO mark(mark) VALUES " + request)
            conn.commit()
        else:
            mark = ["Дефекта нет"]
            mark_range = range(1, len(mark))
            request = ",".join("('%s')" % x for x in mark)
            cursor.execute("INSERT INTO mark(mark) VALUES " + request)
            conn.commit()

        instruction_photo = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]

        domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]

        letters = string.ascii_lowercase[:7]

        date = datetime.date(random.randint(int(datetime.datetime.now().year), int(datetime.datetime.now().year) + 20),
                             random.randint(1, 12), random.randint(1, 28))

        catalog = [random.choice(name_range)]
        cursor.execute(f"INSERT INTO catalog(name) VALUES ('{catalog[0]}')")
        conn.commit()

        medicine = [random.choice(name_range), random.choice(shape_range), random.choice(group_range),
                    random.choice(manufacturers_range), random.randint(1000000000, 9999999999),
                    random.choice(instruction_photo)]
        cursor.execute(
            f"INSERT INTO medicine(name_key, shape_key, group_key, manufacturer_key, barcode, comments) VALUES ({medicine[0]}, {medicine[1]}, {medicine[2]}, {medicine[3]},'{medicine[4]}','{medicine[5]}')")
        conn.commit()

        party = [random.randint(1, 10000), random.choice(name_range), random.randint(1, 10000),
                 random.uniform(100.00, 200.00), random.uniform(300.00, 400.00), date, date, date,
                 random.choice(defect_range), random.choice(mark_range), random.choice(employees_range)]
        cursor.execute(
            f"INSERT INTO medicine(numberparty, medicine_key, count, price, pricepharm, datestart, datefinish, datefact, defect, mark_key, employee_key) VALUES ('{party[0]}', {party[1]}, '{party[2]}', '{party[3]}', '{party[4]}', '{party[5]}', '{party[6]}', '{party[7]}', '{party[8]}', '{party[9]}', {party[10]}, {party[11]})")
        conn.commit()

        pharmacy = [random.choice(pharmacies_range), random.randint(1, 10000), random.choice(type_range),
                    random.choice(district_range), random.choice(address_range) + random.randint(1, 100),
                    random.randint(1000000000, 9999999999)]
        cursor.execute(
            f"INSERT INTO pharmacy(pharmacy, number, type_key, district_key, addresspharm, phone) VALUES ('{pharmacy[0]}', {pharmacy[1]}, '{pharmacy[2]}', {pharmacy[3]},'{pharmacy[4]}','{pharmacy[5]}')")
        conn.commit()

        employee = [random.choice(employees_range), random.choice(pharmacies_range)]
        cursor.execute(f"INSERT INTO employee(employee, pharmacy_key) VALUES ('{employee[0]}', {employee[1]})")
        conn.commit()

        manufacturer = [random.choice(manufacturers_range), random.choice(country_range),
                        random.choice(letters) + "@" + random.choice(domains),
                        random.randint(1900, int(datetime.datetime.now().year))]
        cursor.execute(
            f"INSERT INTO pharmacy(manufacturer, country_key, email, address, yearfirm) VALUES ('{manufacturer[0]}', {manufacturer[1]}, '{manufacturer[2]}', '{manufacturer[3]}','{manufacturer[4]}')")
        conn.commit()

        # Эти строки-будущие запросы к БД. Пример запроса с массива INSERT INTO КУДА(СПИСОК ПОЛЕЙ) VALUES (значения поля 1,поля2,поля3)
        catalog = ""
        medicine = ""
        party = ""
        pharmacy = ""
        employee = ""
        manufacturer = ""

        gen_step = round(gen_range / 12)
        pool = multiprocessing.Pool(12)
        res = pool.starmap_async(self.loop_pool, [(catalog, medicine, party, pharmacy, employee, manufacturer,
                                                   name_range, shape_range, group_range, manufacturers_range,
                                                   instruction_photo, defect_range, mark_range, employees_range,
                                                   pharmacies_range, type_range, district_range, address_range,
                                                   country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step), (
                                                      catalog, medicine, party, pharmacy, employee, manufacturer,
                                                      name_range, shape_range, group_range, manufacturers_range,
                                                      instruction_photo, defect_range, mark_range, employees_range,
                                                      pharmacies_range, type_range, district_range, address_range,
                                                      country_range, letters, domains, gen_step)])
        results = res.get()
        pool.close()
        pool.join()

        catalog = results[0][0] + results[1][0] + results[2][0] + results[3][0] + results[4][0] + results[5][0] + \
                  results[6][0] + results[7][0] + results[8][0] + results[9][0] + results[10][0] + results[11][0]
        medicine = results[0][1] + results[1][1] + results[2][1] + results[3][1] + results[4][1] + results[5][1] + \
                   results[6][1] + results[7][1] + results[8][1] + results[9][1] + results[10][1] + results[11][1]
        party = results[0][2] + results[1][2] + results[2][2] + results[3][2] + results[4][2] + results[5][2] + \
                results[6][2] + results[7][2] + results[8][2] + results[9][2] + results[10][2] + results[11][2]
        pharmacy = results[0][3] + results[1][3] + results[2][3] + results[3][3] + results[4][3] + results[5][3] + \
                   results[6][3] + results[7][3] + results[8][3] + results[9][3] + results[10][3] + results[11][3]
        employee = results[0][4] + results[1][4] + results[2][4] + results[3][4] + results[4][4] + results[5][4] + \
                   results[6][4] + results[7][4] + results[8][4] + results[9][4] + results[10][4] + results[11][4]
        manufacturer = results[0][5] + results[1][5] + results[2][5] + results[3][5] + results[4][5] + results[5][5] + \
                       results[6][5] + results[7][5] + results[8][5] + results[9][5] + results[10][5] + results[11][5]

        query = "INSERT INTO catalog(name) VALUES " + catalog
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO medicine(name_key, shape_key, group_key, manufacturer_key, barcode, comments) VALUES " + medicine
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO medicine(numberparty, medicine_key, count, price, pricepharm, datestart, datefinish, datefact, defect, mark_key, employee_key) VALUES " + party
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO pharmacy(pharmacy, number, type_key, district_key, addresspharm, phone) VALUES " + pharmacy
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO employee(employee, pharmacy_key) VALUES " + employee
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO pharmacy(manufacturer, country_key, email, address, yearfirm) VALUES " + manufacturer
        cursor.execute(query[:-1])
        conn.commit()

    # кнопка "Поиск"
    def Search(self):
        pass

    # кнопка "Удалить"
    def Delete(self):
        match self.choice_table.currentText():
            case "Каталог":
                self.widget_catalog22()
            case "Лекарства":
                self.widget_medicine22()
            case "Партия":
                self.widget_party22()
            case "Аптеки":
                self.widget_pharmacy22()

    # виджет для удаления записей каталога
    def widget_catalog22(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Delete from catalog")
        conn.commit()

    # виджет для удаления записей лекарств
    def widget_medicine22(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Delete from medicine")
        conn.commit()

    # виджет для удаления записей партии
    def widget_party22(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Delete from party")
        conn.commit()

    # виджет для удаления записей аптек
    def widget_pharmacy22(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Delete from pharmacy")
        conn.commit()


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
        start_time = time.time()
        alp = ["а","б","в","г","д","е","ё","ж","з","и","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","э","ю","я"]
        workers = []
        res = []
        for i in alp:
            self.cursor.execute(f"Select avg(summ) from contract inner join client on contract.client_key=client.client_key where client.fio like '{i}%'")
            try:
                res.append(int(self.cursor.fetchone()[0]))
            except:
                res.append(0)
        workers.append(alp)
        workers.append(res)
        workbook = xlsxwriter.Workbook(f'export/workers_final_request_export.xlsx')
        worksheet = workbook.add_worksheet()
        i = 0
        for t in range(len(alp)):
            worksheet.write(i, 0, str(workers[0][t]).strip())
            worksheet.write(i, 1, str(workers[1][t]).strip())
            i += 1
        workbook.close()
        print("--- %s seconds ---" % (time.time() - start_time))

        fig, ax = plt.subplots(figsize=(15, 10))
        ax.pie(res, labels=alp,autopct='%1.1f%%')
        plt.savefig('pie.png')
        fig, bx = plt.subplots(figsize=(15, 10))
        bx.bar(alp, res, color='blue')
        plt.savefig('bar.png')
        t = print_file()
        t.load_image('pie.png')
        t.exec_()
        os.remove('pie.png')
        y = print_file()
        y.load_image('bar.png')
        y.exec_()
        os.remove('bar.png')

    # кнопка "Сохранить"
    def Save(self):
        pass


# форма добавить запись
class Ui_add_note_window(QtWidgets.QDialog, add_note_window.Ui_add_note_window):
    def __init__(self, conn, cursor):
        super().__init__()
        self.setupUi(self)
        self.button_save.clicked.connect(self.save_note)

        self.components2()

    # компоненты комбобоксов
    def components2(self):
        self.choice_manufacturer.addItems(
            ["Производство медикаментов", "Канонфарма продакшн", "Реплек фарм", "Балканфарма", "Гедеон рихтер",
             "Синтез"])
        self.choice_name.addItems(["Фенитоин", "Тримипрамин", "Пирацетам", "Спазмалгон", "Медиана", "Стрептомицин"])
        self.choice_release.addItems(["Таблетка", "Капсула", "Порошок", "Мазь", "Сироп", "Пиллюля"])
        self.choice_pharmacology.addItems(
            ["Противоэпилептическое средство", "Антидепрессант", "Ноотропное средство", "Обезбаливающее средство",
             "Гормональное средство", "Антибиотик"])

        self.button_save.pressed.connect(self.changer2)

    # кейсы комбобоксов
    def changer2(self):
        match self.choice_manufacturer.currentText():
            case "Производство медикаментов":
                self.save_note()
            case "Канонфарма продакшн":
                self.save_note()
            case "Реплек фарм":
                self.save_note()
            case "Балканфарма":
                self.save_note()
            case "Гедеон рихтер":
                self.save_note()
            case "Синтез":
                self.save_note()
        match self.choice_name.currentText():
            case "Фенитоин":
                self.save_note()
            case "Тримипрамин":
                self.save_note()
            case "Пирацетам":
                self.save_note()
            case "Спазмалгон":
                self.save_note()
            case "Медиана":
                self.save_note()
            case "Стрептомицин":
                self.save_note()
        match self.choice_release.currentText():
            case "Таблетка":
                self.save_note()
            case "Капсула":
                self.save_note()
            case "Порошок":
                self.save_note()
            case "Мазь":
                self.save_note()
            case "Сироп":
                self.save_note()
            case "Пиллюля":
                self.save_note()
        match self.choice_pharmacology.currentText():
            case "Противоэпилептическое средство":
                self.save_note()
            case "Антидепрессант":
                self.save_note()
            case "Ноотропное средство":
                self.save_note()
            case "Обезбаливающее средство":
                self.save_note()
            case "Гормональное средство":
                self.save_note()
            case "Антибиотик":
                self.save_note()

    # кнопка "Сохранить"
    def save_note(self):
        if not self.choice_manufacturer.currentText() == "" and not self.choice_name.currentText() == "" and not self.choice_release.currentText() == "" and not self.choice_pharmacology.currentText() == "" and not self.instruction_memo.text() == "" and not self.barcode.text():
            conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                    port=5432)
            cursor = conn.cursor()
            cursor.executemany(
                f"select manufacturer_key from manufacturer where manufacturer={self.choice_manufacturer.currentText()}")
            manufacturer = cursor.fetchall()[0][0]
            cursor.executemany(f"select name_key from catalog where name={self.choice_name.currentText()}")
            name = cursor.fetchall()[0][0]
            cursor.executemany(f"select shape_key from shape where shape={self.choice_release.currentText()}")
            shape = cursor.fetchall()[0][0]
            cursor.executemany(f"select group_key from grouppharm where group={self.choice_pharmacology.currentText()}")
            group = cursor.fetchall()[0][0]
            cursor.executemany(
                f"insert into general(manufacturer_key,name_key, shape_key, "
                f"group_key, instruction_memo, barcode) values ({manufacturer},{name},{shape},{group},"
                f"{self.instruction_memo.text()},{self.barcode.text()})")
            try:
                cursor.executemany()
                conn.commit()
            except Exception as e:
                print(e)


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

        self.components3()

    # компоненты комбобоксов
    def components3(self):
        self.choice_pharmacy.addItems(["Здоровье", "Дарница", "Ольвия"])
        self.choice_district.addItems(["Куйбышевский", "Калининский", "Ворошиловский"])
        self.choice_number.addItems(["233", "141", "305"])
        self.choice_address.addItems(["проспект Ленина, д.43", "улица Заречная, д.105", "улица Агрегатная, д.1а"])

        self.button_ok.pressed.connect(self.changer3)

    # кейсы комбобоксов
    def changer3(self):
        match self.choice_pharmacy.currentText():
            case "Здоровье":
                self.widget_form()
        match self.choice_district.currentText():
            case "Куйбышевский":
                self.widget_form()
        match self.choice_number.currentText():
            case "233":
                self.widget_form()
        match self.choice_address.currentText():
            case "проспект Ленина, д.43":
                self.widget_form()
        match self.choice_pharmacy.currentText():
            case "Дарница":
                self.widget_form2()
        match self.choice_district.currentText():
            case "Калининский":
                self.widget_form2()
        match self.choice_number.currentText():
            case "141":
                self.widget_form2()
        match self.choice_address.currentText():
            case "улица Заречная, д.105":
                self.widget_form2()
        match self.choice_pharmacy.currentText():
            case "Ольвия":
                self.widget_form3()
        match self.choice_district.currentText():
            case "Ворошиловский":
                self.widget_form3()
        match self.choice_number.currentText():
            case "305":
                self.widget_form3()
        match self.choice_address.currentText():
            case "улица Агрегатная, д.1а":
                self.widget_form3()

    # виджет составной формы (показ поставок для первой аптеки)
    def widget_form(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from party where party_key = 1")
        conn.commit()
        self.tableWidget.clear()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(12)
        labels = ['Партия', 'Номер партии', 'Название лекарства', 'Количество упаковок', 'Цена(партия)', 'Цена(аптека)',
                  'Дата выпуска', 'Дата окончания', 'Дата поступления', 'Наличие дефекта', 'Причина возврата',
                  'Сотрудник']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget.resizeColumnsToContents()

    # виджет составной формы (показ поставок для второй аптеки)
    def widget_form2(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from party where party_key = 2")
        conn.commit()
        self.tableWidget.clear()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(12)
        labels = ['Партия', 'Номер партии', 'Название лекарства', 'Количество упаковок', 'Цена(партия)', 'Цена(аптека)',
                  'Дата выпуска', 'Дата окончания', 'Дата поступления', 'Наличие дефекта', 'Причина возврата',
                  'Сотрудник']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget.resizeColumnsToContents()

    # виджет составной формы (показ поставок для третьей аптеки)
    def widget_form3(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                port=5432)
        cursor = conn.cursor()
        cursor.execute(f"Select * from party where party_key = 3")
        conn.commit()
        self.tableWidget.clear()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(12)
        labels = ['Партия', 'Номер партии', 'Название лекарства', 'Количество упаковок', 'Цена(партия)', 'Цена(аптека)',
                  'Дата выпуска', 'Дата окончания', 'Дата поступления', 'Наличие дефекта', 'Причина возврата',
                  'Сотрудник']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        i = 0
        for elem in rows:
            j = 0
            for t in elem:
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.tableWidget.resizeColumnsToContents()

        # date = self.date_expiration.date()
        # print(date)
        # cursor.execute(f"Select datefact from party where datefact = '%s", self.date_expiration.date())


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
