from datetime import datetime, date, time
from dateutil.parser import parse
import os
from pathlib import Path
import view
import model
import global_data
import csv_db_connect

def run() : 
    # global int_db_structure
    # global next_ID
    # print(f"Модуль controller.py, метод run(), next_ID = {global_data.next_ID}")
    # print(f"Модуль controller.py, метод run(), string 13. int_db_structure = \n{global_data.int_db_structure}\n")
    view.out(global_data.HELLO_MESSAGE)
    onward = True
    file_is_OK = csv_db_connect.db_init()
    
    if file_is_OK == global_data.FAIL: # Возникли проблемы с открытием/созданием файла, указанного пользователем
        view.out(global_data.PROGRAM_IS_FINISHING)
        onward = False
    elif file_is_OK == 0 : # Файл с определен, надо проверить его на пустоту
        stat_result = os.stat(global_data.data_base_name)
    #   если исходный файл базы данных не пуст:
        if stat_result.st_size != 0 : 
            reading_attempt, global_data.int_db_structure = model.read_data_from_csv(global_data.data_base_name)
            if reading_attempt in global_data.FLAGS.values() : 
                onward = False
            else : 
                print("Вот исходное состояние файла: \n")
                view.print_all_notes()
                global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
            # print("Считали данные из файла с заметками. ")
            # print(f"Модуль controller.py, метод run(), string 22. int_db_structure = \n{global_data.int_db_structure}\n")
            # print(f"Модуль controller.py, метод run(), string 23. next_ID = {global_data.next_ID}")
            # print(f"Количество заметок в исходном файле = {len(global_data.int_db_structure)}")
        else: 
            view.out(global_data.FILE_WITH_NOTES_IS_EMPTY)
    
    # Файл с заметками считан, можно приступать к работе. 
    
    while onward : 
        view.out(global_data.MAIN_MENU)
        action = view.string_input("  ===> ").strip().lower()
        match action :
            case global_data.MENU: 
                view.out(global_data.COMMANDS_LIST)

            case global_data.LIST: 
                # print("--------------------------Вот все ваши заметки:-----------------------------\n")
                view.print_all_notes()

            case global_data.ADD: 
                note_data = request_note_data()
                # print(f"Type of note_data = {type(note_data)}")
                # print(note_data[0])
                # print(note_data[1])
                # print(f"Длина int_db_structure = {len(global_data.int_db_structure)}")
                model.add_note(note_data[0], note_data[1])
                global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
                # print(f"Длина int_db_structure после выполнения метода add_note = {len(global_data.int_db_structure)}")
                # print(f"Новый next_ID = {global_data.next_ID}")
                #print(f"Type of added_note = {type(added_note)}")
                #  used_ID = added_note[0]
                view.out("В базу добавлена заметка c ID = {}:\n".format(global_data.next_ID-1))
                # print("*************************************************************")
                # print("Печать заметки как есть: ")
                # print(global_data.int_db_structure[-1])
                # print("Печать после преобразования в список строк: ")
                view.print_note(model.note_for_print(global_data.int_db_structure[-1]))
                #  print("Печать неподготовленной заметки: ")
                #  view.print_note(global_data.int_db_structure[-1])
                # view.print_all_notes()

            case global_data.FIND: 
                if not len(global_data.int_db_structure) == 0 : 
                    user_choice = view.string_input(global_data.SEARCH_OPTIONS)
                    if user_choice == global_data.SEARCH_BY_ID: 
                        id_to_show = view.id_input("Введите ID заметки:\n ===> ")
                        if id_to_show != global_data.FAIL :
                            note_to_show = model.get_note_by_id(id_to_show)
                            if note_to_show != [] : 
                                view.out("Заметка с индексом {} имеет вид: \n".format(id_to_show))
                                view.print_note(model.note_for_print(note_to_show))
                        else : 
                            view.out(global_data.NO_SUCH_NOTE)

                    elif user_choice == global_data.SEARCH_BY_HEADER: 
                        header_to_find = view.string_input("Введите название заметки \n" + 
                                    "(если точно не помните, лучше воспользоваться поиском по фрагменту):\n ===> ")
                        notes_to_show = model.get_notes_by_header(header_to_find)
                        if notes_to_show != [] : 
                            view.out(global_data.SEARCH_RESULT)
                            view.print_notes(notes_to_show)
                        else : 
                            view.out(global_data.NO_SUCH_NOTES)

                    elif user_choice == global_data.SEARCH_BY_FRAGMENT: 
                        fragment_to_find = view.string_input("Введите фрагмент, по которому надо искать:\n ===> ")
                        notes_to_show = model.get_notes_by_fragment(fragment_to_find)
                        if notes_to_show != [] : 
                            view.out(global_data.SEARCH_RESULT)
                            view.print_notes(notes_to_show)
                        else : 
                            view.out(global_data.NO_SUCH_NOTES)

                    elif user_choice == global_data.SEARCH_BY_DATE: 
                        date_to_find = view.string_input("Введите дату:\n ===> ")
                        search_result = model.get_notes_by_date(date_to_find)
                        if search_result[0] == global_data.SUCCESS : 
                            if len(search_result[1]) != 0 : 
                                view.out(global_data.SEARCH_RESULT)
                                view.print_notes(search_result[1])
                            else : 
                                view.out(global_data.NO_SUCH_NOTES)

                    else : 
                        view.out(global_data.INVALID_INPUT)
                        view.out(global_data.SEARCH_WILL_NOT_BE_PERFORMED)
                else : 
                    view.out(global_data.LIST_OF_NOTES_IS_EMPTY)
                    
            case global_data.EDIT: 
                if not len(global_data.int_db_structure) == 0 : 
                    to_do = view.choice_of_two("Вы знаете ID заметки, которую хотите редактировать?", f"{global_data.YES} - если  знаете", 
                                   f"{global_data.NO} - если вам надо просмотреть список заметок")
                    if to_do == global_data.YES or to_do == global_data.NO:
                        if to_do == global_data.NO : 
                            view.print_all_notes()
                        id_to_modify = view.string_input("Введите ID заметки, в которую хотите внести изменения:\n ===> ")
                        ind = model.get_ind_of_note_with_id(int(id_to_modify)) 
                        # print(ind)
                        if ind == global_data.FAIL : 
                            view.out(global_data.NO_SUCH_NOTE)
                        else : 
                            view.out(global_data.FOUND_NOTE)
                            view.print_note(model.note_for_print(global_data.int_db_structure[ind]))

                            user_choice = view.string_input(global_data.EDIT_OPTIONS)

                            if user_choice == global_data.CHANGE_HEADER: 
                                new_header = view.string_input("Введите новый заголовок:\n ===> ")
                                if new_header != "" : 
                                    # ind = model.get_ind_of_note_with_id(int(id_to_modify))
                                    global_data.int_db_structure[ind][1] = new_header
                                    view.out(f"\nЗаголовок заметки c ID = {id_to_modify} изменен: \n")
                                    # view.out(f"\nИндекс = {ind}\n")
                                    view.print_note(model.note_for_print(global_data.int_db_structure[ind]))
                                else: 
                                    view.out(global_data.EMPTY_STRING_IS_INPUT)
                                    view.out(global_data.NOTE_WILL_STAY_UNCHANGED)

                            elif user_choice == global_data.CHANGE_TEXT: 
                                new_body = view.string_input("Введите новый текст заметки:\n ===> ")
                                if new_body != "" :  
                                    global_data.int_db_structure[ind][2] = new_body
                                    view.out(f"Текст заметки c ID = {id_to_modify} изменен: ")
                                    view.print_note(model.note_for_print(global_data.int_db_structure[ind]))
                                else: 
                                    view.out(global_data.EMPTY_STRING_IS_INPUT)
                                    view.out(global_data.NOTE_WILL_STAY_UNCHANGED)

                            else: 
                                view.out(global_data.INVALID_INPUT)
                    else : 
                        view.out(global_data.INVALID_INPUT)
                else : 
                    view.out(global_data.LIST_OF_NOTES_IS_EMPTY)

            case global_data.DELETE: 
                if len(global_data.int_db_structure) != 0 : 
                    to_do = view.choice_of_two("Вы знаете ID заметки, которую хотите удалить?", 
                                               f"{global_data.YES} - если  знаете", 
                                               f"{global_data.NO} - если вам надо просмотреть список заметок")
                    if to_do == global_data.NO or to_do == global_data.YES:
                        if to_do == global_data.NO : 
                            view.print_all_notes()
                        id_to_delete = view.string_input("Введите ID заметки, которую хотите удалить:\n ===> ")
                        ind = model.get_ind_of_note_with_id(int(id_to_delete)) 
                        if ind == global_data.FAIL : 
                            view.out(global_data.NOTE_WITH_SUCH_ID_IS_ABSENT)
                        else : 
                            view.out(f"Заметка с ID = {id_to_delete}:\n")
                            view.print_note(model.note_for_print(model.remove_note_with_id(int(id_to_delete))[1]))
                            view.out("УСПЕШНО УДАЛЕНА")
                    else : 
                        view.out(global_data.INVALID_INPUT)
                else : 
                    view.out(global_data.LIST_OF_NOTES_IS_EMPTY)

            case global_data.WRITE_CHANGES_TO_THE_INITIAL_FILE: 
                if csv_db_connect.write_changes_to_data_base() != global_data.SUCCESS :
                    view.out("\nНе удалось выполнить запись в файл {}".format(global_data.data_base_name))
                else : 
                    view.out(f"\nЗапись в файл {global_data.data_base_name} прошла успешно")

            case global_data.SAVE_DATA_TO_ANOTHER_FILE: 
                flag, file_name = csv_db_connect.write_changes_to_another_csv_file()
                if flag == global_data.FAIL :
                    view.out(f"\nНе удалось выполнить запись в файл {file_name}")
                else : 
                    view.out(f"\nЗапись в файл {file_name} прошла успешно")

            case global_data.READ_DATA_FROM_FILE : 
                result, new_file_name = csv_db_connect.get_name_of_existing_csv_file()
                if result == global_data.FLAGS["Not .csv file"] : 
                    view.out(global_data.NOT_CSV_FILE)
                elif result == global_data.FLAGS["Such file doesn't exist"] : 
                    view.out(global_data.SUCH_FILE_DOES_NOT_EXIST)
                else : 
                    flag_of_result, list_of_notes = model.read_data_from_csv(new_file_name)
                    if flag_of_result == 0 :
                        if len(list_of_notes) == 0 : 
                            answer = view.choice_of_two("Данный файл пуст. Вы хотите продолжить с ним работу? ", 
                                                    f"{global_data.YES} - Да, хочу", f"{global_data.NO} - Нет, не хочу")
                            if answer == global_data.YES : 
                                global_data.data_base_name = new_file_name
                                global_data.int_db_structure = list_of_notes
                                global_data.next_ID = 1
                            else : 
                                print(f"...Продолжаем работу с файлом {global_data.data_base_name}")
                        else : 
                            global_data.data_base_name = new_file_name
                            global_data.int_db_structure = list_of_notes 
                            # ОТЛАДОЧНАЯ ПЕЧАТЬ
                            print("Вот исходное состояние файла, с которым Вы пожелали работать: \n")
                            print(global_data.int_db_structure)
                            # ОТЛАДОЧНАЯ ПЕЧАТЬ
                            global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
                
            case global_data.QUIT: 
                onward = False

            case _ : 
                view.out(global_data.INVALID_COMMAND_TRY_AGAIN)

# Функция запрашивает у пользователя данные для создания заметки: 
# - название
# - текст
def request_note_data() : 
    return view.string_input(global_data.NOTE_NAME_INVIT), view.string_input(global_data.NOTE_BODY_INVIT)






    

    
