import ftplib
import random
import sys
from datetime import datetime

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

def loop_pool (branches, workers, gen_range) :
    for i in range(0, gen_range):
        #Вот тут садамия с +=. Мы добавляем за 1 итерация в каждую строку по 1 записи. получается 10000 проходов=10000 строк в КАЖДОЙ ТАБЛИЦЕ
        # random.choice(dict). Когда у тебя есть справочник ты можешь выбрать случайное значение из него этой командой
        #random.randint(от,до). Когда нужно взять число в диапазоне от и до
        #datetime.date(np.random.randint(1900,2000), np.random.randint(1, 12), np.random.randint(1, 28)) Случайная дата от 1900 до 2000 года. Коряво, но я сделал так и в скорости не потерял)))
        branches += f"(1,'{random.choice(np_dictionary)}','{random.choice(np_dictionary)} {random.choice(np_dictionary)} {np.random.randint(1, 200)}',{np.random.choice(city_range)},{random.randint(1000000000, 9999999999)},{np.random.randint(date, datetime.datetime.now().year)}),"
        workers += f"('{random.choice(np_dictionary)}',{np.random.randint(1, gen_range)}),"
        contracts += f"({np.random.randint(1, gen_range)},{np.random.choice(insurance_range)},'{datetime.date(np.random.randint(2000, datetime.datetime.now().year-1), np.random.randint(1, 12), np.random.randint(1, 28))}',{np.random.randint(1, gen_range)},{np.random.randint(1, gen_range)},'{random.choice(photos)}'),"
        clients += f"('{random.choice(np_dictionary)}',{np.random.choice(city_range)},'{datetime.date(np.random.randint(1900, datetime.datetime.now().year-18 ), np.random.randint(1, 12), np.random.randint(1, 28))}','{random.choice(np_dictionary)} {random.choice(np_dictionary)} {np.random.randint(1, 200)}',{np.random.choice(social_range)},{random.randint(1000000000, 9999999999)}),"
    return np.array([branches,workers,contracts,clients])# Именно так ты возвращаешь строку. Тоесть создаётся массив в котором 4 элемента и каждый элемент это строки эти только созданные.
    #ВНИМАНИЕ! Мы в эту функцию передаём не строки с прошлыми запросами а пустые строки из функции в классе. Зачем нам таскать прошлые процессы с собой?

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

    # кнопка "Генерация"
    def Generate(self):
        gen_range = 10000#СКОЛЬКО СТРОК
        #ДАЛЕЕ НАЧИНАЕМ ЗАПОЛНЯТЬ СПРАВОЧНИКИ. НАША ЗАДАЧА ЗАПОЛНИТЬ СПРАВОЧНИКИ ЗАВЕДОМО КОРРЕКТНОЙ ИНФОРМАЦИЕЙ
        self.cursor.execute("TRUNCATE social_dict,city_dict,insurance_dict,property_dict RESTART IDENTITY CASCADE")
        self.conn.commit()
        city = ["Донецк", "Макеевка", "Енакиево", "Кировское", "Торез", "Ждановка", "Амвросиевка", "Красный лиман",
                "Орехово", "Харцызск", "Тельманово", "Ростов-на-Дону", "Киев", "Харьков", "Луцк", "Гонконг", "Чианжи",
                "Шанхай", "Гуанчжоу", "Пекин"]
        city_range = range(1, len(city))
        request = ",".join("('%s')" % x for x in city)
        self.cursor.execute("INSERT INTO city_dict(city) VALUES " + request)
        self.conn.commit()
        social = ["Доход ниже 50 000", "Доход выше 50 000"]
        social_range = range(1, len(social))
        request = ",".join("('%s')" % x for x in social)
        self.cursor.execute("INSERT INTO social_dict(social) VALUES " + request)
        self.conn.commit()
        insurance = ["Страхование личное", "Страхование имущества", "Страхование ответственности",
                     " Страхование финансовых рисков"]
        insurance_range = range(1, len(insurance))
        request = ",".join("('%s')" % x for x in insurance)
        self.cursor.execute("INSERT INTO insurance_dict(insurance_type) VALUES " + request)
        self.conn.commit()
        property = ["Частная", "Общая", "Государственная"]
        property_range = range(1, len(property))
        request = ",".join("('%s')" % x for x in property)
        self.cursor.execute("INSERT INTO property_dict(property) VALUES " + request)
        self.conn.commit()
        #ЗАКОНЧИЛИ ЗАПОЛНЯТЬ СПРАВОЧНИКИ

        photos = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]        #СПИСОК ПУТЕЙ ДЛЯ ФОТО

        date = datetime.date(random.randint(int(datetime.datetime.now().year), int(datetime.datetime.now().year) + 20),
                             random.randint(1, 12), random.randint(1, 28))
        array_general = [random.choice(city_range), random.choice(property_range),
                         random.randint(1000000000, 9999999999),
                         random.choice(np_dictionary) + " " + random.choice(np_dictionary) + " " + str(
                             random.randint(1, 200)),
                         random.choice(np_dictionary), random.randint(1000, 999999999),
                         random.choice(photos), date, random.randint(1900, int(datetime.datetime.now().year))]
        query = r"INSERT INTO general_(city_key,property_key,numberr,address,name_company,number_license,photo,date_open,year_open) VALUES ({},{},{},'{}','{}','{}','{}','{}',{})".format(
            array_general[0], array_general[1], array_general[2], array_general[3], array_general[4], array_general[5],
            array_general[6], array_general[7], array_general[8])
        self.cursor.execute(query)
        self.conn.commit()
        # На данном моменте мы заполнили главный офис(array_general)
        branches = ""
        workers = ""
        contracts = ""
        clients = ""
        #Эти строки-будущие запросы к БД.
        #Пример запроса с массива INSERT INTO КУДА(СПИСОК ПОЛЕЙ) VALUES (значения поля 1,поля2,поля3)

        gen_step = round(gen_range / 12)#Вот тут интереснее. делим вся нашу задачу на количество ядер. я задал их константами
        # У тебя поидее 12 ядер,значит каждое ядро будет считать (количество строк в бд/12)

        pool = multiprocessing.Pool(4)# Создаём пул(пул это объединение потоков)
        res = pool.starmap_async(loop_pool, [(branches,workers,gen_step), (branches,workers,gen_step), (branches, workers,gen_step), (branches,workers,gen_step)])
        #Синтаксис res = pool.starmap_async(loop_pool, [(параметры 1),(параметры 2)]).  код слева запустит в нашем пуле 2 задачи.
        # У тебя задач будет столько же сколько и ядер. Тоесть [()] и круглых скобок внутри 12.
        # Тоесть 2 функции на доступных ядрах. Если будет 24 функции то 12 твоих ядер посчитают сначала первые 12 потом остальные 12. Т.К. Имеется идентификатор
        # async , значит потоки никого не ждут и каждый поток старается сделать быстро и красиво
        # ВНИМАНИЕ. В функцию мы передаем ещё и крайние границы массива. Этого можно избежать, но у меня оно было завязано на рандоме. Тебе можно не делать так.
        #Код выше исправлен и суть работает. Тебе нужно 12 раз передать параметры функциям. Так как у тебя в таблицах связь со справочниками передавай СПРАВОЧНИКИ
        #Чтобы передавать справочники выше я писал массивы ["","",""] из строк Например city,photos и тд. Повторяй за мной. Меняй названия переменных и готов))
        results = res.get()
        #Получние массива ответов(return)
        #Вид типа       ответ1,ответ2,ответ3
        #               ответ1,ответ2,ответ3
        #               ответ1,ответ2,ответ3
        pool.close()
        pool.join()
        #Оставь эти 2 строки без внимания, они просто работают и просто нужны чтобы потом потоки завершились корректно

        # СЮДА СМОТРИШЬ ПОСЛЕ ТОГО КАК ГЛЯНЕШЬ ФУКНЦИЮ НА 71 СТРОКЕ
        branches = results[0][0] + results[1][0] + results[2][0] + results[3][0]
        workers = results[0][1] + results[1][1] + results[2][1] + results[3][1]
        contracts = results[0][2] + results[1][2] + results[2][2] + results[3][2]
        clients = results[0][3] + results[1][3] + results[2][3] + results[3][3]
        # Соответственно у нас массив rusults состоит из массивов в каждом из которых строки под индексами.
        # Смотри как оно работает. второй индекс это индекс строки(в каком порядке ретурн работает так и тут). Тоесть у нас бранчес возвращался первым значит от 0.
        # ВНИМАНИЕ!!!!!!!!!!!!!!!!!!!!!!!!  У меня тут всего 4 строки. Так как было 4 процесса. Ты создаёшь 12 процессов и тут будет огромная таблица [0][0],[0][1],[0][2],[0][3],[0][4] и так до 11!!!!

        #ИНТЕРЕСНО! Тут у нас в строки добавляется наши значения из функций многопотока. Тоесть допустим функция вернула "(1 ", "2 ", "3 ", "4)"
        # Значит у нас будет соединение строк и строка будет (1 2 3 4)
        query = "INSERT INTO branch(general_key,name_branch,address,city,number_branch,year_branch) VALUES " + branches
        #СМ СИНТАКСИС ЗАПРОСОВ ВЫШЕ!!!!!!!!!!!!!!!!!!!!!!!!
        # Запрос к бд+ наши длиныне строки (1,'Корвалол',1234),(2,'Аспирин',4321),..............................
        self.cursor.execute(query[:-1])
        self.conn.commit()
        query = "INSERT INTO workers(FIO,branch_key) VALUES " + workers
        self.cursor.execute(query[:-1])
        self.conn.commit()
        query = "INSERT INTO contract(summ,insurance_key,date,client_key,worker_key,text) VALUES " + contracts
        self.cursor.execute(query[:-1])
        self.conn.commit()
        query = "INSERT INTO client(fio,city_key,date_birthday,address,social_key,number) VALUES " + clients
        self.cursor.execute(query[:-1])
        self.conn.commit()

        #o = ok() Тут у меня открывается окно об успешном завершении
        #o.exec_()


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
