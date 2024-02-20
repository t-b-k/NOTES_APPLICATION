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
    # print(f"Преобразованная заметка: \n{printable_note}")
    return printable_note

# Метод ищет в списке заметок заметку с ID=id и возвращает ее индекс.
# Если такой заметки нет, возвращает -1
def get_ind_of_note_with_id(id) : 
    ind = -1
    for i in range(len(global_data.int_db_structure)) : 
        if int(global_data.int_db_structure[i][0]) == id : 
            ind = i
    print(f"Искомый индекс заметки равен {ind}")
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

# Метод ищет заметку по ее ID
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_note_by_id(id_to_show) : 
    ind = get_ind_of_note_with_id(id_to_show)
    result = global_data.int_db_structure[ind] if ind != -1 else []
    return result

# Метод ищет в списке заметок заметку с заданным заголовком и возвращает ее индекс.
# Если такой заметки нет, возвращает -1
def get_ind_of_note_with_header(header) : 
    ind = -1
    for i in range(len(global_data.int_db_structure)) : 
        if global_data.int_db_structure[i][1] == header : 
            ind = i
    return ind

# Метод ищет заметку по ее заголовку
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_note_by_header(header_to_show) : 
    ind = get_ind_of_note_with_header(header_to_show)
    result = global_data.int_db_structure[ind] if ind != -1 else []
    return result

# Метод ищет в списке заметок заметку, содержащую заданный фрагмент текста в заголовке или в теле, и возвращает ее индекс.
# Если такой заметки нет, возвращает -1
def get_ind_of_note_with_fragment(fragment) : 
    ind = -1
    for i in range(len(global_data.int_db_structure)) : 
        if global_data.int_db_structure[i][1].find(fragment) != -1 or global_data.int_db_structure[i][2].find(fragment) != -1: 
            ind = i
    return ind

# Метод ищет заметку по фрагменту
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_note_by_fragment(fragment_to_find) : 
    ind = get_ind_of_note_with_fragment(fragment_to_find)
    result = global_data.int_db_structure[ind] if ind != -1 else []
    return result

# Метод ищет в списке заметок заметки, созданные в определенную дату, и возвращает список их индексов.
# Если таких заметок нет, возвращает пустой список
def get_ind_of_note_with_date(date_to_find) : 
    result = []
    for i in range(len(global_data.int_db_structure)) : 
        print(parse(global_data.int_db_structure[i][3]).date())
        if parse(global_data.int_db_structure[i][3]).date() == date_to_find.date() :
            result.append(i)
    return result

# Метод ищет заметки по фрагменту
# Возвращает их список или пустой список, если таких заметок нет в базе   
def get_notes_by_date(date_to_find) : 
    result = []
    inds = get_ind_of_note_with_date(date_to_find)
    for i in inds : 
        result.append(global_data.int_db_structure[i])
    return result

