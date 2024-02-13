import os
from pathlib import Path
from datetime import datetime, date, time
from dateutil.parser import parse
from global_data import *
import view

# DEFAULT_DATABASE_FILE_NAME = "notes.csv"
# DEFAULT_PATH_TO_DATA_BASE = os.getcwd()

# FULL_DEFAULT_DATABASE_FILE_NAME = os.path.join(DEFAULT_PATH_TO_DATA_BASE, DEFAULT_DATABASE_FILE_NAME)
# print(type(FULL_DEFAULT_DATABASE_FILE_NAME))
# print(FULL_DEFAULT_DATABASE_FILE_NAME)

def db_init() : 
    global data_base_name
    new_or_existing = view.choice_of_two("Вы будете работать с уже существующим .csv-файлом заметок или хотите создать новый?", 
                       "работать с уже существующим", "создать новый")
    if new_or_existing == 1 : 
        default_or_other = view.choice_of_two(DEFAULT_DB_NAME_MESSAGE, "использовать файл по умолчанию", "использовать другой файл")
        if default_or_other == 2 : 
            user_input = view.in_string("Введите имя файла, с которым хотите работать: ")
            if os.path.exists(user_input) and os.isfile(user_input) : 
                data_base_name = user_input
            else : 
                view.out("Файла с таким именем не существует. Программа завершает работу...")
                return False
        elif default_or_other != 1 : 
            view.out("Вы ввели недопустимое значение. Программа завершает работу... ")
            return False
    elif new_or_existing == 2 : 
        user_choice = view.choice_of_two("Файл с заметками следует создать в текущем каталоге? ", "Да", "Нет")
        if user_choice == 2 : 
            db_path_name = view.in_string(f"Введите путь к каталогу, в котором хотите создать файл или Enter.\nПо умолчанию будет использоваться"+
                                   " каталог: {DEFAULT_PATH_TO_DATA_BASE}")
            if db_path_name == "" : 
                db_path_name = DEFAULT_PATH_TO_DATA_BASE
            elif not os.path.exists(Path(db_path_name)) or not os.path.isdir(Path(db_path_name)): 
                view.out("Каталога с таким именем не существует. Программа завершает работу...")
                return False
            db_file_name = os.path.join(view.in_string("Введите имя нового файла без расширения. Ему будет присвоено расширение .csv: "), 
                                        ".csv")
            data_base_name = os.path.join(db_path_name, db_file_name)
        else : 
            view.out("Вы дали недопустимый ответ. Программа завершает работу... ")
            return False
    else : 
        view.out("Вы ввели недопустимое значение. Программа завершает работу... ")
        return False
    view.out("БД заметок с именем {} готова к работе.".format())
    return True

# Метод db_file_exists проверяет переданную в него строку на то, является ли она корректным 
# полным именем существующего файла
def db_file_exists (full_file_name) : 
    if os.path.exists(full_file_name) : 
        print(f"Файл '{full_file_name}' существует")
        return True
    else : 
        print(f"Файл '{full_file_name}' не существует")
        return False


# Метод db_file_is_csv определяет, является ли поданная на вход строка именем файла с расширением .csv
def db_file_is_csv (file_name) :
    base, ext = os.path.splitext(file_name)
    print("Base:", base)
    print("Extension:", ext)
    return ext[-4:].lower() == ".csv"

    # return file_name[-4:].lower() == ".csv"

date_and_time = datetime.now()
d_and_t_in_str_format = str(date_and_time)
print(d_and_t_in_str_format)
print("Тип переменной d_and_t_in_str_format = {}".format(type(d_and_t_in_str_format)))
print("Тип переменной date_and_time = {}".format(type(date_and_time)))
print(str(date_and_time)[:16]) # Дата + время без секунд и миллисекунд

# Метод чтения данных из .csv-файла с разделителем ';', возвращающий 
# список списков, в котором каждый элемент вложенного списка является строкой. 
# Предполагается, что .csv-файл не содержит заголовков, то есть в возвращаемой структуре 
# "голые" данные
def read_data_from_csv_file (name_of_existing_csv_file) : 
    data = open(name_of_existing_csv_file, 'r', encoding = 'utf-8')
    list_of_lists_of_strings = [[*string.split(sep=";")[0:]] for string in data.readlines()]
    data.close()
    return list_of_lists_of_strings

# Метод записи данных из списка списков строк в .csv-файл с разделителем ';', возвращающий 
# True - если запись прошла успешно; 
# False - при возникновении ошибки
def write_data_to_csv_file (name_of_file, list_of_list_of_strings) : 
    dest = open(name_of_file, 'w', encoding = 'utf-8')
    line_to_write = ""
    for each_line in list_of_list_of_strings : 
        line_to_write = ";".join(each_line)
        line_to_write = line_to_write.join("\n")
        dest.write()


# Метод проверяет, представляет ли собой поданная ему на вход структура списком списков из 4-х строк: 
# def if_read_data_are_notes (data) :
#     if type(data) == list : 
#         # состоит ли данный список из списков: 
#         result = True
#         for elem in data : 
#             result = result and type(elem) == list and len(elem) == 4
#             if result == False : 
#                 return result
#             else : 
#                 for field in elem : 
#                     result = result and type(field) == str
#                 if result == False : 
#                     return result
#                 else : 
#                     date_time = parse(elem[0])
#                     result = elem[0].isdigit() and elem[3][:10].
#         return result
#     else : 
#         return False

print(f"Файл с именем {data_base_name} существует." if db_file_exists(data_base_name) else f"Файла с именем {data_base_name} не существует.")
print("А существует ли файл C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.t ?" , end = " - " )
print(db_file_exists("C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.txt"))
print()
print("А является ли файл C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\Konkurs.csv csv-файлом?" , end = " - " )
print(db_file_is_csv(Path("Konkurs.csv")))

read_file_result = read_data_from_csv_file (data_base_name)
print(type(read_file_result))

# print(f"Является ли содержимое файла заметками? - {if_read_data_are_notes(read_file_result)}")

# print("Konkurs.csv"[-4:])
# data = open(data_file_name, 'r', encoding = 'utf-8')
# print(f"Тип переменной data = {type(data)}")


# notes = [[int(string.split(sep=";")[0]), *string.split(sep=";")[1:]] for string in data.readlines()]
# for elem in notes : 
#     if elem[-1][-1] == '\n' : 
#         elem[-1] = elem[-1][:-1]
# print(type(notes)) 
# print(notes)
# data.close()

# new_data = open("result.csv", 'w', encoding='utf-8')
# for elem in notes : 
#     string_for_file = str(elem[0])+";"
#     for i in elem[1:-1] : 
#         string_for_file = string_for_file + i + ";"
#     string_for_file = string_for_file + elem[-1] + '\n'
#     new_data.write(string_for_file)

# for elem in notes : 
#     if elem[1][3][-1] == "\n" :
#         elem[1][3] = time(elem[1][3][:-1])
# print(notes)
# data_base_model = {(int(fields[0]), fields[1:]) for fields in (next_string.split(sep=";")) for next_string in notes}
# for next_string in notes : 
#     fields = next_string.split(sep=";")
#     print(fields)
#     print(int((next_string.split(sep=";"))[0]))
#     data_base_model[int(fields[0])] = fields[1:]
#print(data_base_model)

