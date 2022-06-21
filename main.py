import ftplib
import multiprocessing
import random
import sys
from datetime import datetime
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
        pass

    # Почему в скобках ты передаешь только branches и workers?
    # loop_pool позже, сначала хочу разобраться с построением генерации
    def loop_pool(branches, workers, gen_range):
        for i in range(0, gen_range):
            branches += f"(1,'{random.choice(np_dictionary)}','{random.choice(np_dictionary)} {random.choice(np_dictionary)} {np.random.randint(1, 200)}',{np.random.choice(city_range)},{random.randint(1000000000, 9999999999)},{np.random.randint(date, datetime.datetime.now().year)}),"
            workers += f"('{random.choice(np_dictionary)}',{np.random.randint(1, gen_range)}),"
            contracts += f"({np.random.randint(1, gen_range)},{np.random.choice(insurance_range)},'{datetime.date(np.random.randint(2000, datetime.datetime.now().year - 1), np.random.randint(1, 12), np.random.randint(1, 28))}',{np.random.randint(1, gen_range)},{np.random.randint(1, gen_range)},'{random.choice(photos)}'),"
            clients += f"('{random.choice(np_dictionary)}',{np.random.choice(city_range)},'{datetime.date(np.random.randint(1900, datetime.datetime.now().year - 18), np.random.randint(1, 12), np.random.randint(1, 28))}','{random.choice(np_dictionary)} {random.choice(np_dictionary)} {np.random.randint(1, 200)}',{np.random.choice(social_range)},{random.randint(1000000000, 9999999999)}),"
        return np.array([branches, workers, contracts,
                         clients])

    # кнопка "Генерация"
    def Generate(self):
        conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port=5432)
        cursor = conn.cursor()
        gen_range = 10000
        cursor.execute("TRUNCATE country, district, employee, grouppharm, mark, shape, type, catalog RESTART IDENTITY CASCADE")
        conn.commit()

        names = ["Фенитоин", "Тримипрамин", "Пирацетам", "Спазмалгон", "Медиана", "Стрептомицин"]
        name_range = range(1, len(names))
        request = ",".join("('%s')" % x for x in names)
        cursor.execute("INSERT INTO catalog(names) VALUES " + request)
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

        employee = ["Безуглый В.В.", "Золотовский М.В.", "Зинатулин А.В."]
        employee_range = range(1, len(employee))
        request = ",".join("('%s')" % x for x in employee)
        cursor.execute("INSERT INTO employee(employee) VALUES " + request)
        conn.commit()

        grouppharm = ["Противоэпилептическое средство", "Антидепрессант", "Ноотропное средство",
                      "Обезбаливающее средство", "Гормональное средство", "Антибиотик"]
        grouppharm_range = range(1, len(grouppharm))
        request = ",".join("('%s')" % x for x in grouppharm)
        cursor.execute("INSERT INTO grouppharm(grouppharm) VALUES " + request)
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

        manufacturer = ["Производство медикаментов", "Канонфарма продакшн", "Реплек фарм", "Балканфарма",
                        "Гедеон рихтер", "Синтез"]
        manufacturer_range = range(1, len(manufacturer))
        request = ",".join("('%s')" % x for x in manufacturer)
        cursor.execute("INSERT INTO manufacturer(manufacturer) VALUES " + request)
        conn.commit()

        # Есть такое поле как "Наличие дефекта" (defect), оно может быть либо "да", либо "нет" (boolean). К нему
        # привязан справочник "Причина возврата" (mark) тоже boolean, который работает таким образом:
        # ЕСЛИ наличие дефекта == да, то вызывается справочник причина возврата, в котором будут генерироваться такие
        # поля, как ["Испорчена упаковка", "Просрочен", "Не хватает медикаментов"]. ЕСЛИ наличие дефекта == нет,
        # то справочник выдает одно поле ["Дефекта нет"]"

        # if defect == 0:
        #      mark = ["Испорчена упаковка", "Просрочен", "Не хватает медикаментов"]
        #      mark_range = range(1, len(mark))
        #      request = ",".join("('%s')" % x for x in mark)
        #      cursor.execute("INSERT INTO mark(mark) VALUES " + request)
        #      conn.commit()
        # else:
        #      mark = ["Дефекта нет"]

        instruction_photo = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]

        # Что мне делать с этим datetime? У меня, например, питон не воспринимает его, возможно, стоит создать что-то?
        date = datetime.date(random.randint(int(datetime.datetime.now().year), int(datetime.datetime.now().year) + 20),
                             random.randint(1, 12), random.randint(1, 28))

        # Почему medicine игнорируется и подчеркивается?
        medicine = [random.choice(name_range), random.choice(shape_range), random.choice(manufacturer_range), random.randint(1000000000, 9999999999), random.choice(instruction_photo)]
        query = r"INSRET INTO medicine_(name_key, shape_key, group_key, manufacturer_key, barcode, comments) VALUES ({}, {}, {}, {},'{}','{}')".format(medicine[0], medicine[1], medicine[2], medicine[3], medicine[4], medicine[5]))
        cursor.execute(query)
        conn.commit()
        # Теперь мне заполнять таким образом следующие таблицы, верно?

        # Эти строки-будущие запросы к БД. Пример запроса с массива INSERT INTO КУДА(СПИСОК ПОЛЕЙ) VALUES (значения поля 1,поля2,поля3)
        # Что это значит? Ты имеешь в виду, что туда нужно будет вставлять запросы к БД?
        # Или мы не трогаем эти строки, просто для понимания оставляем, что там будут будущие запросы?
        branches = ""
        workers = ""
        contracts = ""
        clients = ""

        gen_step = round(
            gen_range / 12)

        # Верно сделала?
        pool = multiprocessing.Pool(12)
        res = pool.starmap_async(loop_pool, [(names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark),
                                             (names, country, district, employee, grouppharm, shape, type, manufacturer, gen_step, mark)])

        results = res.get()
        pool.close()
        pool.join()

        # Верно сделала?
        branches = results[0][0] + results[1][0] + results[2][0] + results[3][0] + results[4][0] + results[5][0] + results[6][0] + results[7][0] + results[8][0] + results[9][0] + results[10][0] + results[11][0]
        workers = results[0][1] + results[1][1] + results[2][1] + results[3][1] + results[4][1] + results[5][1] + results[6][1] + results[7][1] + results[8][1] + results[9][1] + results[10][1] + results[11][1]
        contracts = results[0][2] + results[1][2] + results[2][2] + results[3][2] + results[4][2] + results[5][2] + results[6][2] + results[7][2] + results[8][2] + results[9][2] + results[10][2] + results[11][2]
        clients = results[0][3] + results[1][3] + results[2][3] + results[3][3] + results[4][3] + results[5][3] + results[6][3] + results[7][3] + results[8][3] + results[9][3] + results[10][3] + results[11][3]

        #Этот кусочек я поняла, сделаю его уже как разберусь с тем, что выше
        query = "INSERT INTO branch(general_key,name_branch,address,city,number_branch,year_branch) VALUES " + branches
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO workers(FIO,branch_key) VALUES " + workers
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO contract(summ,insurance_key,date,client_key,worker_key,text) VALUES " + contracts
        cursor.execute(query[:-1])
        conn.commit()
        query = "INSERT INTO client(fio,city_key,date_birthday,address,social_key,number) VALUES " + clients
        cursor.execute(query[:-1])
        conn.commit()

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
