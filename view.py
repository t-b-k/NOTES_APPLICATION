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

def print_note (list_of_4_strigs) : 
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]
    print(tabulate(list_of_4_strigs, headers=columns))

def print_all_notes() : 
    columns = ["ID", "Заголовок", "Текст заметки".ljust(50), "Дата/время создания"]