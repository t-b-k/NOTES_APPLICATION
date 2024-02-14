from datetime import datetime, date, time
from model import int_db_structure, next_ID
import view
import model
from global_data import *
from csv_db_connect import *

READING_ERROR = "ОШИБКА ЧТЕНИЯ ДАННЫХ"

def run() : 
    global int_db_structure, next_ID
    print(f"Модуль controller.py, метод run(), next_ID = {next_ID}")
    view.out(HELLO_MESSAGE)
    onward = True
    notes_exist = db_init()
    if notes_exist == -1: 
        onward = False
    elif notes_exist == 1 : 
        int_db_structure = model.read_data_from_csv(data_base_name)
        print(f"Количество заметок в исходном файле = {len(int_db_structure)}")
        if len(int_db_structure) == 0 : 
            print(READING_ERROR)
        else : 
            print("Ваши заметки: \n")
            print(int_db_structure)
    
    # Файл с заметками определен
    view.out(MAIN_MENU)
    while onward : 
         action = view.string_input("  ===> ")
         match action :
             case 'm': 
                 view.out(COMMANDS_LIST)
             case 'l': 
                 print("Ваши заметки: \n")
                 print(int_db_structure)
             case 'a': 
                 note_data = request_note_data()
                 print(f"Type of note_data = {type(note_data)}")
                 print(note_data[0])
                 print(note_data[1])
                 print(f"Длина int_db_structure = {len(int_db_structure)}")
                 model.add_note("Таня", "Наша Таня громко плачет")
                 print(f"Длина int_db_structure после выполнения метода add_note = {len(int_db_structure)}")
                 print(f"Новый next_ID = {next_ID}")
                 #print(f"Type of added_note = {type(added_note)}")
                #  used_ID = added_note[0]
                 view.out("В базу добавлена заметка c ID = {}:".format(next_ID-1))
                 view.out(model.note_to_string(int_db_structure[-1]))
    #         case 'f': 
    #             onward = False
    #         case 'e': 
    #             onward = False
    #         case 'd': 
    #             onward = False
    #         case 'c': 
    #             onward = False
    #         case 's': 
    #             onward = False
             case 'q': 
                onward = False
             case _ : 
                view.out("Недопустимая команда. Попробуйте еще раз.")

def request_note_data() : 
    return view.string_input(NOTE_NAME_INVIT), view.string_input(NOTE_BODY_INVIT)

# def db_init() : 
#     global data_base_name
#     new_or_existing = view.choice_of_two("Вы будете работать с уже существующим .csv-файлом заметок или хотите создать новый?", 
#                        "работать с уже существующим", "создать новый")
#     if new_or_existing == 1 : 
#         default_or_other = view.choice_of_two(DEFAULT_DB_NAME_MESSAGE, "использовать файл по умолчанию", "использовать другой файл")
#         if default_or_other == 2 : 
#             user_input = view.in_string("Введите имя файла, с которым хотите работать: ")
#             if os.path.exists(user_input) and os.isfile(user_input) : 
#                 data_base_name = user_input
#             else : 
#                 view.out("Файла с таким именем не существует. Программа завершает работу...")
#                 return False
#         elif default_or_other != 1 : 
#             view.out("Вы ввели недопустимое значение. Программа завершает работу... ")
#             return False
#     elif new_or_existing == 2 : 
#         user_choice = view.choice_of_two("Файл с заметками следует создать в текущем каталоге? ", "Да", "Нет")
#         if user_choice == 2 : 
#             db_path_name = view.in_string(f"Введите путь к каталогу, в котором хотите создать файл или Enter.\nПо умолчанию будет использоваться"+
#                                    " каталог: {DEFAULT_PATH_TO_DATA_BASE}")
#             if db_path_name == "" : 
#                 db_path_name = DEFAULT_PATH_TO_DATA_BASE
#             elif not os.path.exists(Path(db_path_name)) or not os.path.isdir(Path(db_path_name)): 
#                 view.out("Каталога с таким именем не существует. Программа завершает работу...")
#                 return False
#             db_file_name = os.path.join(view.in_string("Введите имя нового файла без расширения. Ему будет присвоено расширение .csv: "), 
#                                         ".csv")
#             data_base_name = os.path.join(db_path_name, db_file_name)
#         else : 
#             view.out("Вы дали недопустимый ответ. Программа завершает работу... ")
#             return False
#     else : 
#         view.out("Вы ввели недопустимое значение. Программа завершает работу... ")
#         return False
#     view.out("БД заметок с именем {} готова к работе.".format(data_base_name))
#     return True
                






    

    
