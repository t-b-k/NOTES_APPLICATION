import os
from pathlib import Path
from datetime import datetime, date, time
from dateutil.parser import parse

import global_data
import view

# DEFAULT_DATABASE_FILE_NAME = "notes.csv"
# DEFAULT_PATH_TO_DATA_BASE = os.getcwd()

# FULL_DEFAULT_DATABASE_FILE_NAME = os.path.join(DEFAULT_PATH_TO_DATA_BASE, DEFAULT_DATABASE_FILE_NAME)
# print(type(FULL_DEFAULT_DATABASE_FILE_NAME))
# print(FULL_DEFAULT_DATABASE_FILE_NAME)

# Расположение базы данных заметок, используемое по умолчанию

DEFAULT_DB_NAME_MESSAGE = """По умолчанию используется файл notes.csv из текущей директории"""

DEFAULT_PATH_TO_DATA_BASE = Path(os.getcwd())
DEFAULT_DATA_FILE_NAME = "notes.csv"

global_data.data_base_name = str(DEFAULT_PATH_TO_DATA_BASE.joinpath(DEFAULT_DATA_FILE_NAME))
print(global_data.data_base_name)
print(type(str(global_data.data_base_name)))

""" Метод db_init() возвращает: 
        1 - если файл заметок существует и не пуст
        0 - если файл заметок пуст или вновь создан
       -1 - если файла не существует или с ним что-то не так, или пользователь не справился с вводом
    В результате выполнения данного метода присваевается значение глобальной переменной
    global_data.data_base_name"""

def db_init() : 
    new_or_existing = view.choice_of_two("Вы будете работать с уже существующим .csv-файлом заметок или хотите создать новый?", 
                       "1 - работать с уже существующим", "2 - создать новый")
    
    # Если будем работать с существующим файлом: 
    if new_or_existing == global_data.EXISTING_FILE : 
        default_or_other = view.choice_of_two(DEFAULT_DB_NAME_MESSAGE, 
                                              "1 - использовать файл по умолчанию", 
                                              "2 - использовать другой файл")
        
        # Если пользователь хочет указать свой файл: 
        if default_or_other == global_data.OTHER_FILE_NAME : 
            global_data.data_base_name = get_name_of_existing_csv_file()
            if global_data.data_base_name == "" : 
                view.out("Вы ввели имя несуществующего файла.")
                return -1   # Такого файла не существует
            
        # Если пользователь ввел недопустимое значение: 
        elif default_or_other != global_data.DEFAULT_FILE_NAME : 
            view.out("\nВы ввели недопустимое значение. Программа завершает работу... ")
            return -1
        # В противном случае будет использоваться файл по умолчанию. 
    
    # Если пользователь хочет создать новый файл базы заметок: 
    elif new_or_existing == global_data.NEW_FILE : 
        user_choice = view.choice_of_two("\nФайл с заметками следует создать в текущем каталоге? ", "1 - Да", "2 - Нет")
        if user_choice != global_data.WORKING_DIRECTORY and user_choice != global_data.OTHER_DIRECTORY : 
            view.out("\nВы дали недопустимый ответ. Программа завершает работу... ")
            return -1
        # Если хочет создать новый файл в каталоге, отличном от текущего рабочего: 
        elif  user_choice == global_data.OTHER_DIRECTORY :
            db_path_name = view.string_input("Введите путь к каталогу, в котором хотите создать файл, или нажмите Enter.\n", 
                                             "По умолчанию будет использоваться"+f" каталог: {DEFAULT_PATH_TO_DATA_BASE}\n ===> ")
            if db_path_name == "" : 
                db_path_name = DEFAULT_PATH_TO_DATA_BASE
            elif not os.path.exists(Path(db_path_name)) or not os.path.isdir(Path(db_path_name)): 
                view.out("\nКаталога с таким названием не существует. Программа завершает работу...")
                return -1
        else : 
            db_path_name = DEFAULT_PATH_TO_DATA_BASE
            print(f"\nФайл для заметок будет создан в каталоге {DEFAULT_PATH_TO_DATA_BASE}")

        db_file_name = view.string_input("\nВведите имя нового файла заметок без расширения.\n"+
                                                   "Расширение .csv будет присвоено автоматически: \n ===> ")
        db_file_name = db_file_name + ".csv"
        global_data.data_base_name = os.path.join(db_path_name, db_file_name)
        if os.path.exists(Path(global_data.data_base_name)) : 
            view.out("\nТакое имя файла уже существует либо содержит недопустимые символы. Программа завершает работу... ")
            return -1
        else : 
            with open(global_data.data_base_name, "x", encoding = "utf-8") as db: 
                view.out("Создан файл {}".format(global_data.data_base_name))
    else : 
        view.out("\nВы ввели недопустимое значение. Программа завершает работу... ")
        return -1
        
    view.out("\nБД заметок {} готова к работе. Желаем удачи!\n".format(global_data.data_base_name))
    return 0

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
def get_data (name_of_existing_csv_file) : 
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

def get_name_of_existing_csv_file () : 
    user_input = view.string_input("\nВведите имя .csv-файла (включая расширение), с которым хотите работать: ")
    view.out(user_input)
    print("os.path.exists(user_input) = {}\n".format(os.path.exists(user_input)))
    print("os.path.isfile(user_input) = {}\n".format(os.path.isfile(user_input)))
    if os.path.exists(Path(user_input)) and os.path.isfile(Path(user_input)) : 
        print("Пользователь ввел имя файла с расширением: {}".format(os.path.splitext(user_input)))
        if os.path.splitext(Path(user_input))[1] != ".csv" : 
             view.out("\nИзвините, но данная программа предназначена для работы только с файлами .csv\n")
             user_input = ""
    else : 
        view.out("\nФайла с таким именем не существует...")
        user_input = ""
    return user_input

# Функция запрашивает у пользователя имя файла для записи в него результатов. 
# Возвращает введенное пользователем имя, если соответствующий каталог существует и указано расширение .csv
# В противном случае будет возвращена пустая строка

def get_name_of_dest_csv_file () : 
    user_input = view.string_input("\nВведите имя файла c расширением .csv, в который хотите записать данные: ")
    view.out(user_input)
    path_name = os.path.dirname(user_input)
    file_name = os.path.basename(user_input)
    # Если такой каталог существует и введенное пользователем имя файла заканчивается на ".csv" : 
    if file_name.endswith(".csv") : 
        if os.path.exists(os.path.dirname(Path(path_name))) and os.path.dirname(Path(path_name)) != '': 
            return user_input
        elif os.path.dirname(Path(path_name)) == '' : 
            return os.path.join(os.getcwd(), file_name)
        else : 
            return ""
    else : 
        view.out("Введенное Вами имя файла имеет расширение, отличное от \".csv\"")
        return ""


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

print(f"Файл с именем {global_data.data_base_name} существует." if db_file_exists(global_data.data_base_name) 
      else f"Файла с именем {global_data.data_base_name} не существует.")
print("А существует ли файл C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.t ?" , end = " - " )
print(db_file_exists("C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.txt"))
print()
print("А является ли файл C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\Konkurs.csv csv-файлом?" , end = " - " )
print(db_file_is_csv(Path("Konkurs.csv")))

read_file_result = get_data (global_data.data_base_name)
print(type(read_file_result))

# Запись изменений в исходный файл базы данных
def write_changes_to_data_base () : 
    try : 
        with open(global_data.data_base_name, 'w', encoding='utf-8') as db : 
            data_to_write = []
            for note in global_data.int_db_structure : 
                data_to_write.append(";".join(note)+"\n")
            db.writelines(data_to_write)
        return 0
    except :
        view.out(" !!! ОШИБКА ЗАПИСИ")    
        return -1

# Запись/дозапись изменений в заданный файл
def write_changes_to_file (file_name, mode='w') : 
    try :
        with open(file_name, mode, encoding='utf-8') as db : 
            data_to_write = []
            for note in global_data.int_db_structure : 
                data_to_write.append(";".join(note)+"\n")
            db.writelines(data_to_write)
        return 0
    except :
        view.out(" !!! ОШИБКА ЗАПИСИ")    
        return -1

# Запись изменений в другой файл с расширением .csv
# Возвращаем имя файла, в который была произведена запись, или пустую строку в случае неудачи
def write_changes_to_another_csv_file () : 
    file_to_write = get_name_of_dest_csv_file ()
    print(file_to_write)
    if file_to_write == "" : 
        view.out("\n !!! Некорректное имя .csv-файла. Записать изменения в файл не удалось. !!!")
        print("os.path.exists(os.path.dirname(user_input)) = {}".format(os.path.exists(os.path.dirname(file_to_write))))
        print("os.path.exists(user_input) = {}\n".format(os.path.exists(file_to_write)))
        print("os.path.isfile(user_input) = {}\n".format(os.path.isfile(file_to_write)))
        return ""

    # Если файл с введенным именем уже существует: 
    if os.path.exists(Path(file_to_write)) :  
        view.out("Вы ввели имя существующего файла. ")
        view.out("При дозаписи мы не гарантируем, что информация из этого файла сможет быть считана данной программой, ")
        view.out("поскольку он может иметь неправильный формат. Выбирайте дозапись, только если уверены, что файл отформатирован правильно. ")
        user_choice = view.choice_of_two("Перезаписываем файл или дописываем в конец? ", "1 - перезаписываем", "2 - дописываем в конец")
        if user_choice == global_data.REWRITE : 
            return write_changes_to_file(file_to_write)
            
        elif user_choice == global_data.APPEND : 
            return write_changes_to_file(file_to_write, 'a')

        else : 
            view.out("Вы ввели некорректное значение. Завершить операцию не получится. ")
            return -1
    else : 
        view.out("\nФайла с таким именем не существует. Будет создан новый файл. ")
        write_changes_to_file(file_to_write)
        return file_to_write
