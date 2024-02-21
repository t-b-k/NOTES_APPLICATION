# В данном модуле собраны все глобальные переменные

import os
from pathlib import Path
from datetime import datetime, date, time

HELLO_MESSAGE = """**************************************************************************************************************
                       Вас приветствует приложение \"З А М Е Т К И\"
**************************************************************************************************************
С его помощью Вы сможете создать новую базу заметок или продолжить работу с уже существующей.
Для хранения заметок применяется файл формата .csv, в котором под одну заметку отводится одна строка вида: \n
        <ID заметки>;<Заголовок_заметки>;<Текст_заметки>;<Дата&Время создания заметки>\n
Таким образом, символ \";\" выполняет функцию разделителя полей и не может использоваться в тексте полей заметок
**************************************************************************************************************\n"""

NOTE_NAME_INVIT = "Введите заголовок заметки\n ===> "
NOTE_BODY_INVIT = "Введите текст заметки\n ===> "

COMMANDS_LIST = "\n".join(["{:66}{}".format("        m - Просмотреть список доступных команд", "l - Просмотреть все заметки"),
                          "{:66}{}".format("        a - Добавить новую заметку", "f - Найти и просмотреть заметку"),
                          "{:66}{}".format("        e - Редактировать заметку", "d - Удалить заметку"),
                          "{:66}{}".format("        w - Записать изменения в исходный файл базы данных", 
                                           "s - Сохранить изменения в новый файл .csv"),
                          "{:66}{}\n".format("        r - Считать заметки из другого файла .csv", 
                                           "q - Выйти (без сохранения изменений)")])
        # m - Просмотреть список доступных команд
        # l - Просмотреть все заметки
        # a - Добавить новую заметку
        # f - Найти и просмотреть заметку
        # e - Редактировать заметку
        # d - Удалить заметку
        # w - Записать изменения в исходный файл базы данных
        # s - Сохранить изменения в новый файл .csv
        # r - Считать заметки из другого файла .csv
        # q - Выйти (без сохранения изменений)\n"""

MAIN_MENU = """\n***********************************************************************************************************
                                     Выберите действие: """+ "\n" + COMMANDS_LIST + """
**********************************************************************************************************\n"""
MENU = 'm'
READ = 'r'
LIST = 'l'
ADD = 'a'
EDIT = 'e'
DELETE = 'd'
FIND = 'f'
WRITE_CHANGES_TO_THE_INITIAL_FILE = 'w'
SAVE_DATA_TO_ANOTHER_FILE = 's'
READ_DATA_FROM_FILE = 'r'
QUIT = 'q'

REMINDER = """\*Формат заметки: <ID заметки>;<Заголовок_заметки>;<Тело_заметки>;<Дата&Время создания заметки>
(символ \";\" используется для разделения полей и не может содержаться в тексте заметки)"""

# Максимально число попыток, предоставляемых пользователю для ввода правильных данных
MAX_NUMBER_OF_ATTEMPTS = 3

# Инициализируем внутреннюю структуру для хранения заметок в процессе работы пустым списком
int_db_structure = []

# В глобальной переменной next_ID содержится следующий готовый к использованию идентификатор заметки
next_ID = 1

# КОНСТАНТЫ ДЛЯ РАБОТЫ С ФАЙЛАМИ: 
EXISTING_FILE = 1
NEW_FILE = 2
DEFAULT_FILE_NAME = 1
OTHER_FILE_NAME = 2
WORKING_DIRECTORY = 1
OTHER_DIRECTORY = 2
REWRITE = 1
APPEND = 2

# В глобальной переменной data_base_name хранится имя .csv-файла, с которым мы работаем в данном сеансе
data_base_name = ""

print(datetime.today())
print(date.today())
# print(DEFAULT_PATH_TO_DATA_BASE)
# print(type(DEFAULT_PATH_TO_DATA_BASE))

print("Текущая директория:", os.getcwd())
print(os.path.exists(os.getcwd()))
print(os.path.exists(Path("C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION")))
print(os.path.isdir(Path("C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\\notes.csv")))
print(os.path.isfile(Path("C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\\notes.csv")))

"""Для хранения заметок в процессе работы с программой используется список, элементами которого являются заметки. 
   Каждая заметка - это список из 4-х элементов: 
   <ID заметки> - уникальное целое положительное число (идентификатор заметки). 
                  Идентификатор присваивается заметке автоматически в момент создания заметки 
                  и после ее удаления повторно не используется. Файл .csv, в котором не выполнено требования уникальности 
                  идентификаторов, считается имеющим неверный формат, и работа с ним отменяется. 
   <Заголовок_заметки> - Строка из русских и/или латинских букв, цифр и прочих символов, за исключением ';'
   <Тело_заметки> - Строка из русских и/или латинских букв, цифр и прочих символов, за исключением ';'
   <Дата&Время создания заметки> - дата и время создания заметки, присваивается автоматически при создании заметки.
                  Имеет формат, предусмотренный модулем datetime.datetime из библиотеки Python
"""
