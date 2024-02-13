import global_data

def out(what_to_show) : 
    print(what_to_show)

def choice_of_two (question_str, the_first_str, the_second_str) : 
    print(f"{question_str}\n")
    answer = int(input("1 - {}\n2 - {}\n ===> ".format(the_first_str, the_second_str)))
    return answer

def in_string (invit_message) : 
    return input(invit_message)
