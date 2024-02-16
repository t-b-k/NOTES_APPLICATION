from datetime import datetime, date, time
from tabulate import tabulate
from dateutil.parser import parse

import global_data
import view

TYPE_CONVERSION_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: невозможно преобразовать к нужному типу"
NOT_UNIQUE_IDS_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: неуникальные идентификаторы заметок."
WRONG_FIELDS_QTY = "Модуль model.py\n\tОшибка формата файла базы данных: неверное количество полей в заметке."

# Инициализируем внутреннюю структуру для хранения заметок в процессе работы пустым списком
# int_db_structure = []
# В глобальной переменной next_ID содержится следующий по порядку незадействованный идентификатор заметки
# next_ID = 1

def read_data_from_csv (csv_file_name) : 
    # global int_db_structure, next_ID
    empty_list = []
    data = open(csv_file_name, 'r', encoding = 'utf-8')
    list_of_notes = [[*string.split(sep=";")[0:]] for string in data.readlines()]
    for next in list_of_notes : 
        if len(next) != 4 : 
            print(WRONG_FIELDS_QTY)
            return empty_list
        try : 
            next[0] = str(int(next[0])) # преобразовали строку с ID заметки в целое, и затем обратно в строку (для удобства 
                                        # вывода в консоль лучше все хранить в строковом формате)
            next[3] = parse(next[3]).strftime("%d-%m-%Y %H:%M:%S") # преобразовали строку в дату/время и затем  - 
                                                                    # в строку формата dd-mm-YY HH:MM:SS
        except : 
            print(TYPE_CONVERSION_ERROR)
            return empty_list    
    print("СПИСОК ЗАМЕТОК: ")
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
    return max([int(note[0]) for note in list_of_notes]) + 1

def add_note(header, text) : 
    # global next_ID, int_db_structure
    note = [str(global_data.next_ID), header, text, datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    print(type(note))
    print(f"Внутри метода add_note, перед добавлением заметки в list_of_notes ее длина равна {len(global_data.int_db_structure)}")
    global_data.int_db_structure.append(note)
    print(f"Внутри метода add_note, после добавления заметки в list_of_notes ее длина равна {len(global_data.int_db_structure)}")
    # next_ID += 1
    return global_data.int_db_structure[-1]

def note_for_print (note) : 
    printable_note = [(note[0], note[1], note[2], note[3])]
    print(f"Преобразованная заметка: \n{printable_note}")
    return printable_note

# Метод ищет в списке заметок заметку с ID=id и возвращает ее индекс.
# Если такой заметки нет, возвращает -1
def get_ind_of_note_with_id(id) : 
    ind = -1
    for i in range(len(global_data.int_db_structure)) : 
        if int(global_data.int_db_structure[i][0]) == id : 
            ind = i
    return ind

# Метод удаляет из списка заметку с ID=id_to_delete
# Возвращает: 
# 0, если такая заметка найдена и удалена
# -1 - если такой заметки не обнаружено
def remove_note_with_id(id_to_delete) : 
    ind = get_ind_of_note_with_id(id_to_delete)
    if ind == -1 : 
        return -1
    else : 
        global_data.int_db_structure.remove(global_data.int_db_structure[ind])
        return 0






