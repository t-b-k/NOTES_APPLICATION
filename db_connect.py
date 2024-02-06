import os
from pathlib import Path
from datetime import datetime, date, time

DEFAULT_DATA_FILE_NAME = "notes.csv"
DEFAULT_PATH_TO_DATA_BASE = Path(os.getcwd())

data_file_name = str(DEFAULT_PATH_TO_DATA_BASE)+"\\"+DEFAULT_DATA_FILE_NAME

# Метод db_file_exists проверяет переданную в него строку на то, является ли она корректным 
# полным именем существующего файла


# Метод db_file_is_csv определяет, является ли поданная на вход строка именем файла с расширением .csv
def db_file_is_csv (file_name) :
    return file_name[-4:].lower() == ".csv"

date_and_time = datetime.now()
print(type(date_and_time))
print(str(date_and_time)[:16]) # Дата + время без секунд и миллисекунд

# Метод чтения данный из .csv-файла с разделителем ';', возвращающий 
# список списков, в котором каждый элемент вложенного списка является строкой. 
# Предполагается, что .csv-файл не содержит заголовков, то есть в возвращаемой структуре 
# "голые" данные
def read_data_from_csv_file (name_of_existing_csv_file) : 

# print(db_file_is_csv("Konkurs.csv"))
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

