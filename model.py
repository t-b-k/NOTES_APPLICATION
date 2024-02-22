from datetime import datetime, date, time
from tabulate import tabulate
from dateutil.parser import parse

import global_data

import view

# FILE_WITH_NOTES_IS_EMPTY = "!!! ФАЙЛ ПУСТ !!!"
# ILLEGAL_NOTE_ID = "Модуль model.py\n\tОшибка формата файла базы данных: недопустимый идентификатор заметки"
# NEGATIVE_NOTE_ID = "Модуль model.py\n\tОшибка формата файла базы данных: отрицательный идентификатор заметки"
# DATE_TIME_PARSING_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: невозможно распознать дату/время"
# NOT_UNIQUE_IDS_ERROR = "Модуль model.py\n\tОшибка формата файла базы данных: неуникальные идентификаторы заметок."
# WRONG_FIELDS_QTY = "Модуль model.py\n\tОшибка формата файла базы данных: неверное количество полей в заметке."

# Инициализируем внутреннюю структуру для хранения заметок в процессе работы пустым списком
# int_db_structure = []
# В глобальной переменной next_ID содержится следующий по порядку незадействованный идентификатор заметки
# next_ID = 1
# Метод возвращает кортеж: 


def read_data_from_csv (csv_file_name) : 
    # global int_db_structure, next_ID
    empty_list = []
    try :
        data = open(csv_file_name, 'r', encoding = 'utf-8')
    except: 
        view.out("!!! ОШИБКА ЧТЕНИЯ ДАННЫХ. Метод read_data_from_csv(file_name) из модуля model.py !!!")
        return (global_data.FAIL, empty_list)
    list_of_notes = [[*string.split(sep=";")[0:]] for string in data.readlines()]
    
    # if len(list_of_notes) == 0 : 
    #     view.out(FILE_WITH_NOTES_IS_EMPTY)
    #     return (global_data.FLAGS["Source file is empty"], empty_list)
    # Прочитали из файла список списков строк
    for next_note in list_of_notes : 
        # Если какой-то из списков содержит не 4 строки, то это не заметка:
        if len(next_note) != 4 : 
            view.out(global_data.WRONG_FIELDS_QTY)
            return (global_data.FLAGS["Wrong file structure"], empty_list)
        try : 
            next_note[0] = str(int(next_note[0])) # преобразовали строку с ID заметки в целое, и затем обратно в строку (для удобства 
                                        # вывода в консоль лучше все хранить в строковом формате)
        except : 
            view.out(global_data.ILLEGAL_NOTE_ID)
            return (global_data.FLAGS["Illegal note ID"], empty_list)
        if int(next_note[0]) <= 0 : 
            view.out(global_data.NEGATIVE_NOTE_ID)
            return (global_data.FLAGS["Negative note ID"], empty_list)
        try : 
            next_note[3] = parse(next_note[3]).strftime("%d-%m-%Y %H:%M:%S") # преобразовали строку в дату/время и затем  - 
                                                                    # в строку формата dd-mm-YY HH:MM:SS
        except : 
            view.out(global_data.DATE_TIME_PARSING_ERROR)
            return (global_data.FLAGS["Wrong date/time format"], empty_list)
    
    if not all_IDs_are_different(list_of_notes) : 
        view.out(global_data.NOT_UNIQUE_IDS_ERROR)
        return (global_data.FLAGS["Not all IDs are unique"], empty_list)
    
    print("ВОТ СПИСОК ЗАМЕТОК, содержащихся в базе данных: ")
    print(list_of_notes)

    data.close()
    # next_ID = get_next_ID(list_of_notes)
    return (global_data.SUCCESS, list_of_notes)

def all_IDs_are_different(list_of_notes) : 
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
    return ind

# Метод удаляет из списка заметку с ID=id_to_delete
# Возвращает: 
# 0, если такая заметка найдена и удалена
# -1 - если такой заметки не обнаружено
def remove_note_with_id(id_to_delete) : 
    ind = get_ind_of_note_with_id(id_to_delete)
    if ind == global_data.FAIL : 
        return global_data.FAIL
    else : 
        global_data.int_db_structure.remove(global_data.int_db_structure[ind])
        return global_data.SUCCESS

# Метод ищет заметку по ее ID (корректность ID проверяется в методе view.)
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_note_by_id(id_to_show) : 
    ind = get_ind_of_note_with_id(id_to_show)
    result = global_data.int_db_structure[ind] if ind != global_data.FAIL else []
    return result

# Метод ищет в списке заметок заметки с указанным заголовком и возвращает список их индексов.
# Возвращает список индексов таких заметок, пустой, если таких заметок нет
# Поиск нечувствителен к регистру и крайним пробельным символам
def get_inds_of_notes_with_header(header) : 
    result = [i for i in range(len(global_data.int_db_structure)) if 
            global_data.int_db_structure[i][1].strip().lower() == header.strip().lower()]
    return result

# Метод ищет заметки по заголовку
# Возвращает список таких заметок или пустой список, если такой заметки нет в базе   
def get_notes_by_header(header_to_find) : 
    indexes = get_inds_of_notes_with_header(header_to_find) 
    return get_list_of_notes_by_inds(indexes)

# Метод принимает на вход список индексов и возвращает список соответствующих им заметок
def get_list_of_notes_by_inds(list_of_inds) : 
    set_of_inds = set(list_of_inds)
    ordered_inds = sorted(list(set_of_inds))
    return [global_data.int_db_structure[ind] for ind in ordered_inds]

# Метод ищет в списке заметок заметки с указанным фрагментом и передает список их индексов 
# через глобальную переменную global_data.result_list.
# Возвращает 0, если результат поиска ненулевой.
# Если таких заметок нет, возвращает -1
def get_inds_of_notes_with_fragment(fragment) : 
    result = [i for i in range(len(global_data.int_db_structure)) if
        (global_data.int_db_structure[i][1].lower().find(fragment.strip().lower()) != -1 or 
        global_data.int_db_structure[i][2].lower().find(fragment.strip().lower()) != -1)]
    return result

# Метод ищет заметку по фрагменту
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_notes_by_fragment(fragment_to_find) :
    indexes = get_inds_of_notes_with_fragment(fragment_to_find)
    return get_list_of_notes_by_inds(indexes)
    

# Метод ищет в списке заметок заметки, созданные в определенную дату, и возвращает кортеж: 
#   (0, global_data.FAIL - если метод сработал без ошибок
#   (-1, []) - если в процессе выполнения возникла ошибка распознавания какой-либо даты

def get_inds_of_notes_with_date(date_to_find) : 
    result_list = []
    for i in range(len(global_data.int_db_structure)) : 
        try :
            # print(parse(global_data.int_db_structure[i][3]).date())
            if parse(global_data.int_db_structure[i][3]).date() == parse(date_to_find).date() :
                result_list.append(i)
        except : 
            view.out("\n!!! ОШИБКА ФОРМАТА ДАННЫХ !!! Строка не может быть распознана как дата.")
            result_list = []
            return (global_data.FAIL, result_list)
    return (global_data.SUCCESS, result_list)

# Метод возвращает кортеж: 
#   (0, <Список найденных заметок>) - если метод сработал без ошибок
#   (-1, []) - если в процессе его выполнения возникла ошибка распознавания даты
 
def get_notes_by_date(date_to_find) : 
    result = (global_data.FAIL, [])
    search_result = get_inds_of_notes_with_date(date_to_find)
    if search_result[0] == global_data.SUCCESS : 
        result = (global_data.SUCCESS, [global_data.int_db_structure[ind] for ind in search_result[1]])
    return result

