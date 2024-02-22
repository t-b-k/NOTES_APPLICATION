import global_data
from tabulate import tabulate

def out(what_to_show) : 
    print(what_to_show)

def choice_of_two (question_str, the_first_str, the_second_str) : 
    print(f"{question_str}\n")
    answer = int(input(" {}\n {}\n ===> ".format(the_first_str, the_second_str)))
    return answer

def string_input (invit_message) : 
    return input(invit_message)

# Метод int_input возвращает:
# -1 - если введенное пользователем значение не является целым числом, 
# введенное значение - если оно является целым

def int_input (invit_message) : 
    try : 
        user_input = int(input(invit_message))
    except : 
        return -1
    return user_input
    
# Метод id_input возвращает:
# -1 - если введенное пользователем значение не является целым положительным числом, 
# введенное значение - если оно может быть идентификатором заметки

def id_input (invit_message) : 
    try : 
        user_input = int(input(invit_message))
    except : 
        return -1
    return -1 if user_input <= 0 else user_input

def print_note (list_of_4_strigs) : 
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(list_of_4_strigs, headers=columns))
    print()

def print_all_notes() : 
    print("----------------------Вот все ваши заметки: --------------------------------------------------")
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(global_data.int_db_structure, headers=columns))
    print()

def print_notes(list_of_notes) : 
    print("-------------------------------------------------------------------------------------------------")
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(list_of_notes, headers=columns))
    print()