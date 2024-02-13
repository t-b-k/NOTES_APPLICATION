from global_data import *
import view
import csv_db_connect

def run() : 
    view.out(HELLO_MESSAGE)
    
    db_init()
    onward = False
    while onward : 
        view.out(MAIN_MENU)

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
    view.out("БД заметок с именем {} готова к работе.".format(data_base_name))
    return True
    

    
