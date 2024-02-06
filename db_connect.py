import os
from pathlib import Path
from datetime import datetime, date, time

DEFAULT_DATA_FILE_NAME = "notes.csv"
DEFAULT_PATH_TO_DATA_BASE = Path(os.getcwd())

data_file_name = str(DEFAULT_PATH_TO_DATA_BASE)+"\\"+DEFAULT_DATA_FILE_NAME

data = open(data_file_name, 'r', encoding = 'utf-8')
print(f"Тип переменной data = {type(data)}")
# for line in data : 
#     print(line)
notes = [[int(string.split(sep=";")[0]), *string.split(sep=";")[1:]] for string in data.readlines()]
for elem in notes : 
    if elem[-1][-1] == '\n' : 
        elem[-1] = elem[-1][:-1]
print(type(notes)) 
print(notes)
data.close()

new_data = open("result.csv", 'w', encoding='utf-8')
for elem in notes : 
    string_for_file = str(elem[0])+";"
    for i in elem[1:-1] : 
        string_for_file = string_for_file + i + ";"
    string_for_file = string_for_file + elem[-1] + '\n'
    new_data.write(string_for_file)
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

