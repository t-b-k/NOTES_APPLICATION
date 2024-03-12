import os
from pathlib import Path
from datetime import datetime, date, time
from dateutil.parser import parse

import global_data
import view

# Расположение базы данных заметок, используемое по умолчанию

DEFAULT_DB_NAME_MESSAGE = """По умолчанию используется файл notes.csv из текущей директории"""

DEFAULT_PATH_TO_DATA_BASE = Path(os.getcwd())
DEFAULT_DATA_FILE_NAME = "notes.csv"

global_data.data_base_name = str(DEFAULT_PATH_TO_DATA_BASE.joinpath(DEFAULT_DATA_FILE_NAME))
# print(global_data.data_base_name)
# print(type(str(global_data.data_base_name)))

# Метод db_init() возвращает: 
#         0 - если файл заметок существует или вновь создан
#        -1 - если файла не существует или с ним что-то не так, или пользователь не справился с вводом
#     В результате выполнения данного метода присваивается значение глобальной переменной
#     global_data.data_base_name

def db_init() : 
    new_or_existing = view.choice_of_two("Вы будете работать с уже существующим .csv-файлом заметок или хотите создать новый?", 
                       "{} - работать с уже существующим".format(global_data.EXISTING_FILE), 
                       "{} - создать новый".format(global_data.NEW_FILE))
    
    # Если будем работать с существующим файлом: 
    if new_or_existing == global_data.EXISTING_FILE : 
        default_or_other = view.choice_of_two(DEFAULT_DB_NAME_MESSAGE, 
                                              "{} - использовать файл по умолчанию".format(global_data.DEFAULT_FILE_NAME), 
                                              "{} - использовать другой файл".format(global_data.OTHER_FILE_NAME))
        
        # Если пользователь хочет указать свой файл: 
        if default_or_other == global_data.OTHER_FILE_NAME : 
            global_data.data_base_name = get_name_of_existing_csv_file()
            if global_data.data_base_name == "" : 
                view.out("Вы ввели имя несуществующего файла.")
                return global_data.FAIL   # Такого файла не существует
            
        # Если пользователь ввел недопустимое значение: 
        elif default_or_other != global_data.DEFAULT_FILE_NAME : 
            view.out("\nВы ввели недопустимое значение. Программа завершает работу... ")
            return global_data.FAIL
        # В противном случае будет использоваться файл по умолчанию. 
    
    # Если пользователь хочет создать новый файл базы заметок: 
    elif new_or_existing == global_data.NEW_FILE : 
        user_choice = view.choice_of_two("\nФайл с заметками следует создать в текущем каталоге? ", "1 - Да", "2 - Нет")
        if user_choice != global_data.WORKING_DIRECTORY and user_choice != global_data.OTHER_DIRECTORY : 
            view.out("\nВы дали недопустимый ответ. Программа завершает работу... ")
            return global_data.FAIL
        # Если хочет создать новый файл в каталоге, отличном от текущего рабочего: 
        elif  user_choice == global_data.OTHER_DIRECTORY :
            db_path_name = view.string_input("Введите путь к каталогу, в котором хотите создать файл, или нажмите Enter.\n" +
                                             "По умолчанию будет использоваться" +
                                             f" каталог: {DEFAULT_PATH_TO_DATA_BASE}\n ===> ")
            try : 
                if db_path_name == "" : 
                    db_path_name = DEFAULT_PATH_TO_DATA_BASE
                elif not os.path.exists(Path(db_path_name)) or not os.path.isdir(Path(db_path_name)): 
                    view.out("\n"+global_data.NO_SUCH_DIRECTORY+global_data.PROGRAM_IS_FINISHING+"\n")
                    return global_data.FAIL
            except : 
                view.out(global_data.ILLEGAL_PATH_FORMAT)
                return global_data.FAIL
        else : 
            db_path_name = DEFAULT_PATH_TO_DATA_BASE
            print(f"\nФайл для заметок будет создан в каталоге {DEFAULT_PATH_TO_DATA_BASE}")

        db_file_name = view.string_input("\nВведите имя нового файла заметок без расширения.\n"+
                                                   "Расширение .csv будет присвоено автоматически: \n ===> ")
        db_file_name = db_file_name + ".csv"
        try : 
            global_data.data_base_name = os.path.join(db_path_name, db_file_name)
            if os.path.exists(Path(global_data.data_base_name)) : 
                view.out("\n"+global_data.FILE_EXISTS+global_data.PROGRAM_IS_FINISHING+"\n")
                return global_data.FAIL
            else : 
                with open(global_data.data_base_name, "x", encoding = "utf-8") as db: 
                    view.out("Создан файл {}".format(global_data.data_base_name))
        except : 
            view.out(global_data.ILLEGAL_FILE_NAME)    
            return global_data.FAIL
    else : 
        view.out("\n"+global_data.INVALID_INPUT+global_data.PROGRAM_IS_FINISHING+"\n")
        return global_data.FAIL
        
    view.out("\nБД заметок {} готова к работе. Желаем приятной работы!\n".format(global_data.data_base_name))
    return global_data.SUCCESS

# Метод db_file_exists проверяет переданную в него строку на то, является ли она корректным 
# полным именем существующего файла

# def db_file_exists (full_file_name) : 
#     if os.path.exists(full_file_name) : 
#         print(f"Файл '{full_file_name}' существует")
#         return True
#     else : 
#         print(f"Файл '{full_file_name}' не существует")
#         return False


# Метод db_file_is_csv определяет, является ли поданная на вход строка именем файла с расширением .csv
# Возвращает Truе или False
def db_file_is_csv (file_name) :
    base, ext = os.path.splitext(file_name)
    print("Base:", base)
    print("Extension:", ext)
    return ext[-4:].lower() == ".csv"

    # return file_name[-4:].lower() == ".csv"

# date_and_time = datetime.now()
# d_and_t_in_str_format = str(date_and_time)
# print(d_and_t_in_str_format)
# print("Тип переменной d_and_t_in_str_format = {}".format(type(d_and_t_in_str_format)))
# print("Тип переменной date_and_time = {}".format(type(date_and_time)))
# print(str(date_and_time)[:16]) # Дата + время без секунд и миллисекунд

# Метод чтения данных из .csv-файла с разделителем ';', возвращающий 
# список списков, в котором каждый элемент вложенного списка является строкой. 
# Предполагается, что .csv-файл не содержит заголовков, то есть в возвращаемой структуре 
# "голые" данные
def get_data (name_of_existing_csv_file) : 
    data = open(name_of_existing_csv_file, 'r', encoding = 'utf-8')
    list_of_lists_of_strings = [[*string.split(sep=";")[0:]] for string in data.readlines()]
    data.close()
    return list_of_lists_of_strings

# Метод проверки содержимого реально существующего csv-файла на целостность: то есть, 
# что он действительно представляет собой файл с заметками правильного формата



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

# Метод запрашивает у пользователя имя .csv-файла и возвращает его в виде строки

def get_name_of_existing_csv_file () : 
    user_input = view.string_input("\nВведите имя .csv-файла (включая расширение), с которым хотите работать: ")
    # view.out(user_input)
    # print("os.path.exists(user_input) = {}\n".format(os.path.exists(user_input)))
    # print("os.path.isfile(user_input) = {}\n".format(os.path.isfile(user_input)))
    if os.path.exists(Path(user_input)) and os.path.isfile(Path(user_input)) : 
        print("Пользователь ввел имя файла с расширением: {}".format(os.path.splitext(user_input)[1]))
        if os.path.splitext(Path(user_input))[1] != ".csv" : 
             view.out("\nИзвините, но данная программа предназначена для работы только с файлами .csv\n")
             user_input = ""
    else : 
        view.out("\nФайла с таким именем не существует...")
        user_input = ""
    return user_input

# Функция запрашивает у пользователя имя файла для записи в него результатов. 
# Возвращает кортеж: 
# (<Флаг из global_data.FLAGS>, <Полное имя файла с расширением ".csv", 
# соответствующий каталог существует и файл имеет расширение ".csv, или пустая строка (в противном случае)>)
# Если пользователь не ввел расширение, оно будет добавлено автоматически. 

def get_name_of_dest_csv_file () : 
    empty_string = ""
    user_input = view.string_input("\nВведите имя файла c расширением \".csv\", в который хотите записать данные.\n"+
                                   "Если будет введено имя без расширения, оно автоматически будет дополнено расширением \".csv\" ===> ")
    view.out(user_input)
    print(user_input.find("."))
    if user_input.find(".") != global_data.FAIL : 
        if not user_input.endswith(".csv") : 
            return (global_data.FLAGS["Not \".csv\"-extention"], empty_string)
    else : 
        if user_input != "" : 
            user_input = "".join([user_input, ".csv"])
            # ОТЛАДОЧНАЯ ПЕЧАТЬ
            print("user_input = {}\n".format(user_input))
            try : 
                path_name = os.path.dirname(user_input)
                file_name = os.path.basename(user_input)
            except : 
                # view.out(global_data.INVALID_FILE_OR_PATH_NAME)
                return (global_data.FLAGS["Illegal path or file name"], empty_string)
    
            if os.path.exists(os.path.dirname(Path(path_name))) and os.path.dirname(Path(path_name)) != '': 
                return (global_data.SUCCESS, user_input)
            elif os.path.dirname(Path(path_name)) == '' : 
                return (global_data.SUCCESS, os.path.join(os.getcwd(), file_name))
            else : 
                return (global_data.FLAGS["Illegal path or file name"], empty_string)
        else : 
            return (global_data.FLAGS["Illegal file name"], empty_string)
        
# print(f"Файл с именем {global_data.data_base_name} существует." if db_file_exists(global_data.data_base_name) 
#       else f"Файла с именем {global_data.data_base_name} не существует.")
# print("А существует ли файл C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.t ?" , end = " - " )
# print(db_file_exists("C:\\Users\\Татьяна Калашникова\\CODE\\Cheburashka.txt"))
# print()
# print("А является ли файл C:\\Users\\Татьяна Калашникова\\CODE\\NOTES_APPLICATION\Konkurs.csv csv-файлом?" , end = " - " )
# print(db_file_is_csv(Path("Konkurs.csv")))

# read_file_result = get_data (global_data.data_base_name)
# print(type(read_file_result))

# Запись изменений в исходный файл базы данных
def write_changes_to_data_base () : 
    try : 
        with open(global_data.data_base_name, 'w', encoding='utf-8') as db : 
            data_to_write = []
            for note in global_data.int_db_structure : 
                data_to_write.append(";".join(note)+"\n")
            db.writelines(data_to_write)
        return global_data.SUCCESS
    except :
        view.out(" !!! ОШИБКА ЗАПИСИ")    
        return global_data.FAIL

# Запись/дозапись изменений в заданный файл
def write_changes_to_file (file_name, mode='w') : 
    try :
        with open(file_name, mode, encoding='utf-8') as db : 
            data_to_write = []
            for note in global_data.int_db_structure : 
                data_to_write.append(";".join(note)+"\n")
            db.writelines(data_to_write)
        return global_data.SUCCESS
    except :
        view.out(global_data.WRITE_TO_FILE_ERROR)    
        return global_data.FAIL

# Запись изменений в другой файл с расширением .csv
# Возвращаем имя файла, в который была произведена запись, или пустую строку в случае неудачи
def write_changes_to_another_csv_file () : 
    empty_string = ""
    flag, file_to_write = get_name_of_dest_csv_file ()
    if flag == global_data.FLAGS["Not \".csv\"-extention"] : 
        view.out(global_data.ILLEGAL_EXTENTION)
        return global_data.FAIL, empty_string
    elif flag == global_data.FLAGS["Illegal path or file name"] : 
        view.out(global_data.INVALID_FILE_OR_PATH_NAME)
        return global_data.FAIL, empty_string
    # else : 
    # print(file_to_write)
    # if file_to_write == "" : 
    #     view.out("\n !!! Некорректное имя .csv-файла. Записать изменения в файл не удалось. !!!")
    #     print("os.path.exists(os.path.dirname(user_input)) = {}".format(os.path.exists(os.path.dirname(file_to_write))))
    #     print("os.path.exists(user_input) = {}\n".format(os.path.exists(file_to_write)))
    #     print("os.path.isfile(user_input) = {}\n".format(os.path.isfile(file_to_write)))
    #     return ""

    # Если файл с введенным именем уже существует: 
    if os.path.exists(Path(file_to_write)) :  
        view.out("Вы ввели имя существующего файла. ")
        view.out("При дозаписи мы не гарантируем, что информация из этого файла сможет быть считана данной программой, ")
        view.out("поскольку он может иметь неправильный формат. Выбирайте дозапись, только если уверены, что файл отформатирован правильно. ")
        user_choice = view.choice_of_two("Перезаписываем файл или дописываем в конец? ", "1 - перезаписываем", "2 - дописываем в конец")
        if user_choice == global_data.REWRITE : 
            return write_changes_to_file(file_to_write), file_to_write
            
        elif user_choice == global_data.APPEND : 
            return write_changes_to_file(file_to_write, 'a'), file_to_write

        else : 
            view.out("Вы ввели некорректное значение. Завершить операцию не получится. ")
            return global_data.FAIL, empty_string
    else : 
        view.out(global_data.SUCH_FILE_DOES_NOT_EXIST+global_data.NEW_FILE_WILL_BE_CREATED)
        return write_changes_to_file(file_to_write), file_to_write
