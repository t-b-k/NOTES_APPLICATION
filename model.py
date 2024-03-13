from datetime import datetime, date, time
from tabulate import tabulate
from dateutil.parser import parse

import global_data
import view

# Модуль, реализующий внутреннюю структуру для хранения базы данных заметок 
# в ходе работы программы.

# Метод read_data_from_csv (csv_file_name) возвращает кортеж result: 
#   - цифровой результат операции - код ошибки или global_data.SUCCESS - result[0]
#   - список заметок (списков строковых полей) - result[1]
#
# Возможные коды ошибок: 
# global_data.FAIL - не удалось считать данные из файла
# global_data.WRONG_FIELDS_QTY - какая-то из заметок содержит неверное количество полей
# global_data.ILLEGAL_NOTE_ID - поле <идентификатор заметки> содержит не целое число
# global_data.NEGATIVE_NOTE_ID - идентификатор заметки является отрицательным числом
# global_data.DATE_TIME_PARSING_ERROR - содержимое поля "Дата" не может быть преобразовано в дату
# global_data.NOT_UNIQUE_IDS_ERROR - идентификаторы заметок не уникальны

def read_data_from_csv (csv_file_name) : 
    empty_list = []
    try :
        file_with_data = open(csv_file_name, 'r', encoding = 'utf-8')
    except: 
        view.out(global_data.READ_FROM_FILE_ERROR)
        return global_data.FAIL, empty_list
    list_of_notes = [[*string.split(sep=";")[0:]] for string in file_with_data.readlines()]

    # Прочитали из файла список списков строк
    for next_note in list_of_notes : 
        # Если какой-то из списков содержит не 4 строки, то это не заметка:
        if len(next_note) != 4 : 
            view.out(global_data.WRONG_FIELDS_QTY)
            return global_data.FLAGS["Wrong file structure"], empty_list
        try : 
            next_note[0] = str(int(next_note[0])) # преобразовали строку с ID заметки в целое, и затем обратно в строку (для удобства 
                                        # вывода в консоль лучше все хранить в строковом формате)
        except : 
            view.out(global_data.ILLEGAL_NOTE_ID)
            return global_data.FLAGS["Illegal note ID"], empty_list
        if int(next_note[0]) <= 0 : 
            view.out(global_data.NEGATIVE_NOTE_ID)
            return global_data.FLAGS["Negative note ID"], empty_list
        try : 
            next_note[3] = parse(next_note[3]).strftime("%d-%m-%Y %H:%M:%S") # преобразовали строку в дату/время и затем  - 
                                                                    # в строку формата dd-mm-YY HH:MM:SS
        except : 
            view.out(global_data.DATE_TIME_PARSING_ERROR)
            return global_data.FLAGS["Wrong date/time format"], empty_list

    if not all_IDs_are_different(list_of_notes) : 
        view.out(global_data.NOT_UNIQUE_IDS_ERROR)
        return global_data.FLAGS["Not all IDs are unique"], empty_list

    file_with_data.close()
    return global_data.SUCCESS, list_of_notes

# Логический метод проверяет, что все индексы у заметок различны
def all_IDs_are_different(list_of_notes) : 
    set_of_indexes = set([int(note[0].strip()) for note in list_of_notes])
    return len(set_of_indexes) == len(list_of_notes)

# Метод вычисляет первый незанятый ID после максимального в списке заметок, для добавления новых записей
def get_next_ID (list_of_notes) : 
    return max([int(note[0].strip()) for note in list_of_notes]) + 1

# Метод добавляет в список заметок заметку с заданными заголовком и текстом
def add_note(header, text) : 
    note = [str(global_data.next_ID), header, text, datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    global_data.int_db_structure.append(note)
    return global_data.int_db_structure[-1]

# Подготовка заметки к выводу в консоль c помощью tabulate (преобразование в список кортежей, 
# содержащий один кортеж)
def note_for_print (note) : 
    printable_note = [(note[0], note[1], note[2], note[3])]
    return printable_note

# Метод ищет в списке заметок заметку с ID=id и возвращает ее индекс.
# Если такой заметки нет, возвращает global_data.FAIL
def get_ind_of_note_with_id(id) : 
    ind = global_data.FAIL
    for i in range(len(global_data.int_db_structure)) : 
        if int(global_data.int_db_structure[i][0]) == id : 
            ind = i
    return ind

# Метод удаляет из списка заметку с ID=id_to_delete
# Возвращает: 
# 0, если такая заметка найдена и удалена, и удаленную заметку
# global_data.FAIL - если такой заметки не обнаружено, и пустой список
def remove_note_with_id(id_to_delete) : 
    empty_note = []
    ind = get_ind_of_note_with_id(id_to_delete)
    if ind == global_data.FAIL : 
        return global_data.FAIL, empty_note
    else : 
        removed_note = global_data.int_db_structure.pop(ind)
        return global_data.SUCCESS, removed_note

# Метод ищет заметку по ее ID (корректность ID проверяется в методе view)
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_note_by_id(id_to_show) : 
    ind = get_ind_of_note_with_id(id_to_show)
    result = global_data.int_db_structure[ind] if ind != global_data.FAIL else []
    return result

# Метод ищет в списке заметок все заметки с указанным заголовком и возвращает список их индексов.
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

# Метод ищет в списке заметок заметки, содержащие заданный фрагмент текста, и возвращает список их индексов 
def get_inds_of_notes_with_fragment(fragment) : 
    result = [i for i in range(len(global_data.int_db_structure)) if
        (global_data.int_db_structure[i][1].lower().find(fragment.strip().lower()) != -1 or 
        global_data.int_db_structure[i][2].lower().find(fragment.strip().lower()) != -1)]
    return result

# Метод ищет заметки по фрагменту
# Возвращает ее копию или пустой список, если такой заметки нет в базе   
def get_notes_by_fragment(fragment_to_find) :
    indexes = get_inds_of_notes_with_fragment(fragment_to_find)
    return get_list_of_notes_by_inds(indexes)
    

# Метод ищет в списке заметок заметки, созданные в определенную дату, и возвращает кортеж: 
# (-1, <пустой список>) - если строка date_to_find не поддается преобразованию в дату
# (0, <список найденных записей>) - если строка date_to_find успешно преобразована в дату

def get_inds_of_notes_with_date(date_to_find) : 
    result_list = []
    flag = global_data.FAIL
    try : 
        parse(date_to_find).date()
    except : 
            view.out(global_data.STRING_CAN_NOT_BE_PARSED_TO_DATE)
            result_list = []
            return (flag, result_list)
    for i in range(len(global_data.int_db_structure)) : 
        if parse(global_data.int_db_structure[i][3]).date() == parse(date_to_find).date() :
            result_list.append(i)
    flag = global_data.SUCCESS
    return (flag, result_list)

# Метод возвращает кортеж: 
#   (0, <Список найденных заметок>) - если метод сработал без ошибок
#   (-1, []) - если в процессе его выполнения возникла ошибка распознавания даты
 
def get_notes_by_date(date_to_find) : 
    result = (global_data.FAIL, [])
    search_result = get_inds_of_notes_with_date(date_to_find)
    if search_result[0] == global_data.SUCCESS : 
        result = (global_data.SUCCESS, [global_data.int_db_structure[ind] for ind in search_result[1]])
    return result

