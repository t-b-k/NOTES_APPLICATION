import os
from pathlib import Path
from datetime import datetime, date, time
from dateutil.parser import parse

DEFAULT_DATA_FILE_NAME = "notes.csv"
DEFAULT_PATH_TO_DATA_BASE = os.getcwd()

data_file_name = os.path.join(DEFAULT_PATH_TO_DATA_BASE, DEFAULT_DATA_FILE_NAME)
print(type(data_file_name))
print(data_file_name)

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
    data = open(data_file_name, 'r', encoding = 'utf-8')
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


# Метод проверяет, представляет ли собой поданная ему на вход структура список списков из 4-х строк: 
def if_read_data_are_notes (data) :
    if type(data) == list : 
        # состоит ли данный список из списков: 
        result = True
        for elem in data : 
            result = result and type(elem) == list and len(elem) == 4
            if result == False : 
                return result
            else : 
                for field in elem : 
                    result = result and type(field) == str
                if result == False : 
                    return result
                else : 
                    date_time = parse(elem[0])
                    result = elem[0].isdigit() and elem[3][:10].is
        return result
    else : 
        return False

print(db_file_exists(data_file_name))
print(db_file_exists("C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.txt"))
print()
print(db_file_is_csv(Path("Konkurs.csv")))

read_file_result = read_data_from_csv_file (data_file_name)
print(type(read_file_result))

print(f"Является ли содержимое файла заметками? - {if_read_data_are_notes(read_file_result)}")

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

