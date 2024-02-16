from datetime import datetime, date, time
import view
import model
import global_data
import csv_db_connect

READING_ERROR = "ОШИБКА ЧТЕНИЯ ДАННЫХ"

def run() : 
    # global int_db_structure
    # global next_ID
    print(f"Модуль controller.py, метод run(), next_ID = {global_data.next_ID}")
    print(f"Модуль controller.py, метод run(), string 13. int_db_structure = \n{global_data.int_db_structure}\n")
    view.out(global_data.HELLO_MESSAGE)
    onward = True
    notes_exist = csv_db_connect.db_init()
    if notes_exist == -1: 
        onward = False
    elif notes_exist == 1 : 
        global_data.int_db_structure = model.read_data_from_csv(global_data.data_base_name)
        global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
        print("Считали данные из файла с заметками. ")
        print(f"Модуль controller.py, метод run(), string 22. int_db_structure = \n{global_data.int_db_structure}\n")
        print(f"Модуль controller.py, метод run(), string 23. next_ID = {global_data.next_ID}")
        print(f"Количество заметок в исходном файле = {len(global_data.int_db_structure)}")
        if len(global_data.int_db_structure) == 0 : 
            print(READING_ERROR)
        else : 
            print("Ваши заметки: \n")
            print(global_data.int_db_structure)
    
    # Файл с заметками определен
    view.out(global_data.MAIN_MENU)
    while onward : 
         action = view.string_input("  ===> ")
         match action :
             case global_data.MENU: 
                 view.out(global_data.COMMANDS_LIST)
             case global_data.LIST: 
                 print("--------------------------Вот все ваши заметки:-----------------------------\n")
                 view.print_all_notes()
             case global_data.ADD: 
                 note_data = request_note_data()
                 print(f"Type of note_data = {type(note_data)}")
                 print(note_data[0])
                 print(note_data[1])
                 print(f"Длина int_db_structure = {len(global_data.int_db_structure)}")
                 model.add_note(note_data[0], note_data[1])
                 global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
                 print(f"Длина int_db_structure после выполнения метода add_note = {len(global_data.int_db_structure)}")
                 print(f"Новый next_ID = {global_data.next_ID}")
                 #print(f"Type of added_note = {type(added_note)}")
                #  used_ID = added_note[0]
                 view.out("В базу добавлена заметка c ID = {}:".format(global_data.next_ID-1))
                 print("*************************************************************")
                 print("Печать заметки как есть: ")
                 print(global_data.int_db_structure[-1])
                 print("Печать после преобразования в список строк: ")
                 view.print_note(model.note_for_print(global_data.int_db_structure[-1]))
                #  print("Печать неподготовленной заметки: ")
                #  view.print_note(global_data.int_db_structure[-1])
                 view.print_all_notes()
    #         case 'f': 
    #             onward = False
    #         case 'e': 
    #             onward = False
             case global_data.DELETE: 
                 view.print_all_notes()
                 id_to_delete = int(view.string_input("Введите ID заметки, которую хотите удалить: "))
                 if (model.remove_note_with_id(id_to_delete) == -1): 
                     view.out(f"!!! Заметки с ID = {id_to_delete} нет.")
                 else : 
                     view.out(f"!!! Заметка с ID = {id_to_delete} удалена.")
             case global_data.COPY: 
                 onward = False
    #         case 's': 
    #             onward = False
             case 'q': 
                onward = False
             case _ : 
                view.out("Недопустимая команда. Попробуйте еще раз.")

def request_note_data() : 
    return view.string_input(global_data.NOTE_NAME_INVIT), view.string_input(global_data.NOTE_BODY_INVIT)

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
                






    

    
