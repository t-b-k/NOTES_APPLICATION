from datetime import datetime, date, time
from tabulate import tabulate
from dateutil.parser import parse

from global_data import *

TYPE_CONVERSION_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: невозможно преобразовать к нужному типу"
NOT_UNIQUE_IDS_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: неуникальные идентификаторы заметок."
WRONG_FIELDS_QTY = "Модуль model.py\n\tОшибка формата файла базы данных: неверное количество полей в заметке."

# Инициализируем внутреннюю структуру для хранения заметок в процессе работы пустым списком
# int_db_structure = []
# В глобальной переменной next_ID содержится следующий по порядку незадействованный идентификатор заметки
# next_ID = 1

def read_data_from_csv (csv_file_name) : 
    global int_db_structure, next_ID
    empty_list = []
    data = open(csv_file_name, 'r', encoding = 'utf-8')
    list_of_notes = [[*string.split(sep=";")[0:]] for string in data.readlines()]
    for next in list_of_notes : 
        if len(next) != 4 : 
            print(WRONG_FIELDS_QTY)
            return empty_list
        try : 
            next[0] = int(next[0]) # преобразовали строку с ID заметки в целое 
            next[3] = parse(next[3])
        except : 
            print(TYPE_CONVERSION_ERROR)
            return empty_list    
    print("list_of_notes: ")
    print(list_of_notes)
    if not all_IDs_are_diferent(list_of_notes) : 
        print(NOT_UNIQUE_IDS_ERROR)
        return empty_list
    data.close()
    # next_ID = get_next_ID(list_of_notes)
    return list_of_notes

def all_IDs_are_diferent(list_of_notes) : 
    set_of_indexes = set([note[0] for note in list_of_notes])
    return len(set_of_indexes) == len(list_of_notes)

def get_next_ID (list_of_notes) : 
    return max([note[0] for note in list_of_notes]) + 1

def add_note(list_of_notes, next_ID, header, text) : 
    # global next_ID, int_db_structure
    note = [next_ID, header, text, datetime.now()]
    print(type(note))
    print(f"Внутри метода add_note, перед добавлением заметки в list_of_notes ее длина равна {len(list_of_notes)}")
    list_of_notes.append(note)
    print(f"Внутри метода add_note, после добавления заметки в list_of_notes ее длина равна {len(list_of_notes)}")
    # next_ID += 1
    return list_of_notes[-1]

def note_to_string (note) : 
    columns = ["ID", "Заголовок", "Текст", "Дата/время создания"]
    printable_note = [str(note[0]), note[1], note[2], note[3].strftime("%D-%m-%Y %H:%M:%S")]
    # print(tabulate(printable_note, headers=columns))
    # print()
    return printable_note