import global_data
from tabulate import tabulate

# Метод  вывода в консоль сообщения для пользователя: 
def out(what_to_show) : 
    print(what_to_show)

# Метод получения от пользователя цифрового ответа - одного из двух возможных: 
def choice_of_two (question_str, the_first_str, the_second_str) : 
    print(f"{question_str}\n")
    try : 
        answer = int(input(" {}\n {}\n ===> ".format(the_first_str, the_second_str)))       
    except : 
        answer = global_data.FAIL
    return answer

# Получение от пользователя строки через консоль
def string_input (invit_message) : 
    return input(invit_message)
    
# Метод id_input возвращает:
# -1 - если введенное пользователем значение не является целым положительным числом, 
# введенное значение - в противном случае

def id_input (invit_message) : 
    try : 
        user_input = int(input(invit_message))
    except : 
        return global_data.FAIL
    return global_data.FAIL if user_input <= 0 else user_input

# Метод вывода в консоль заметки с заголовками и табуляцией
def print_note (list_of_4_strigs) : 
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(list_of_4_strigs, headers=columns))
    print()

# Метод вывода в консоль всех заметок из текущего состояния БД с заголовками и табуляцией
def print_all_notes() : 
    print("-"*58+"Вот все ваши заметки:"+"-"*58)
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(global_data.int_db_structure, headers=columns))
    print()

# Метод вывода в консоль списка заметок с заголовками и табуляцией
def print_notes(list_of_notes) : 
    print("-"*100)
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(list_of_notes, headers=columns))
    print()