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
        onward = False
    elif file_is_OK == 0 : # Файл с определен, надо проверить его на пустоту
        stat_result = os.stat(global_data.data_base_name)
    #   если исходный файл базы данных не пуст:
        if stat_result.st_size != 0 : 
            reading_attempt, global_data.int_db_structure = model.read_data_from_csv(global_data.data_base_name)
            if reading_attempt in global_data.FLAGS.values() : 
                onward = False
            else : 
                print("Вот исходное состояние файла, с которым Вы пожелали работать: \n")
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
        action = view.string_input("  ===> ").lower()
        match action :
            case global_data.MENU: 
                view.out(global_data.COMMANDS_LIST)

            case global_data.LIST: 
                print("--------------------------Вот все ваши заметки:-----------------------------\n")
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
                user_choice = view.string_input(global_data.SEARCH_OPTIONS)
                if user_choice == global_data.SEARCH_BY_ID: 
                    id_to_show = view.id_input("Введите ID заметки:\n ===> ")
                    if id_to_show != global_data.FAIL :
                        note_to_show = model.get_note_by_id(id_to_show)
                        if note_to_show != [] : 
                            view.out("Заметка с индексом {} имеет вид: \n".format(id_to_show))
                            view.print_note(model.note_for_print(note_to_show))
                    else : 
                        view.out("Заметки с таким ID нет в базе.")

                elif user_choice == global_data.SEARCH_BY_HEADER: 
                    header_to_find = view.string_input("Введите название заметки \n" + 
                                    "(если точно не помните, лучше воспользоваться поиском по фрагменту):\n ===> ")
                    notes_to_show = model.get_notes_by_header(header_to_find)
                    if notes_to_show != [] : 
                        view.out("Найдены заметки: \n")
                        view.print_notes(notes_to_show)
                    else : 
                        view.out("Заметок с таким названием нет в базе.")

                elif user_choice == global_data.SEARCH_BY_FRAGMENT: 
                    fragment_to_find = view.string_input("Введите фрагмент, по которому надо искать:\n ===> ")
                    notes_to_show = model.get_notes_by_fragment(fragment_to_find)
                    if notes_to_show != [] : 
                        view.out("Найдены заметки: \n")
                        view.print_notes(notes_to_show)
                    else : 
                        view.out("Заметок, содержащих такой фрагмент, нет в базе.")

                elif user_choice == global_data.SEARCH_BY_DATE: 
                    date_to_find = view.string_input("Введите дату:\n ===> ")
                    search_result = model.get_notes_by_date(date_to_find)
                    if search_result[0] != global_data.FAIL : 
                        if search_result[1] != [] : 
                            view.out("Найдены заметки: \n")
                            view.print_notes(search_result[1])
                        else : 
                            view.out("Заметок, созданных в указанную Вами дату, нет в базе. ")
                    else : 
                        view.out("\n")

            case global_data.EDIT: 
                to_do = view.choice_of_two("Вы знаете ID заметки, которую хотите редактировать?", "1 - если  знаете", 
                                   "2 - если вам надо просмотреть список заметок")
                if to_do == 2 or to_do == 1:
                    if to_do == 2 : 
                        view.print_all_notes()
                    id_to_modify = view.string_input("Введите ID заметки, в которую хотите внести изменения:\n ===> ")
                    ind = model.get_ind_of_note_with_id(int(id_to_modify)) 
                    # print(ind)
                    if ind == -1 : 
                        view.out("!!! Извините, заметки с таким ID не существует. !!!")
                    else : 
                        view.out("Вок как выглядит заметка, которую Вы хотите отредактировать: \n")
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
                                
                        elif user_choice == global_data.CHANGE_TEXT: 
                            new_body = view.string_input("Введите новый текст заметки:\n ===> ")
                            if new_body != "" :  
                                global_data.int_db_structure[ind][2] = new_body
                                view.out(f"Текст заметки c ID = {id_to_modify} изменен: ")
                                view.print_note(model.note_for_print(global_data.int_db_structure[ind]))
                        else: 
                            view.out("!!! ОШИБКА ВВОДА. Возвращаемся в основное меню !!!")
                else : 
                    view.out("!!! ОШИБКА ВВОДА. Возвращаемся в основное меню !!!")

            case global_data.DELETE: 
                to_do = view.choice_of_two("Вы знаете ID заметки, которую хотите удалить?", "1 - если  знаете", 
                                   "2 - если вам надо просмотреть список заметок")
                if to_do == 2 or to_do == 1:
                    if to_do == 2 : 
                        view.print_all_notes()
                    id_to_delete = view.string_input("Введите ID заметки, которую хотите удалить:\n ===> ")
                    ind = model.get_ind_of_note_with_id(int(id_to_modify)) 
                    # print(ind)
                    if ind == -1 : 
                        view.out("!!! Извините, заметки с таким ID не существует. !!!")
                    else : 
                        
                        view.print_note(model.note_for_print(global_data.int_db_structure[ind]))
                view.print_all_notes()
                id_to_delete = int(view.string_input("Введите ID заметки, которую хотите удалить: "))
                if (model.remove_note_with_id(id_to_delete) == global_data.FAIL): 
                    view.out(f"!!! Заметки с ID = {id_to_delete} нет. !!!")
                else : 
                    view.out(f"!!! Заметка с ID = {id_to_delete} успешно удалена.")

            case global_data.WRITE_CHANGES_TO_THE_INITIAL_FILE: 
                if csv_db_connect.write_changes_to_data_base() != global_data.SUCCESS :
                    view.out("Не удалось выполнить запись в базу данных")
                else : 
                    view.out(f"\nЗапись в файл {global_data.data_base_name} прошла успешно")

            case global_data.SAVE_DATA_TO_ANOTHER_FILE: 
                destination_file = csv_db_connect.write_changes_to_another_csv_file()
                if destination_file == '' :
                    view.out("Не удалось выполнить запись в файл")
                else : 
                    view.out(f"\nЗапись в файл {destination_file} прошла успешно")
            
            case global_data.READ_DATA_FROM_FILE : 
                new_file_name = csv_db_connect.get_name_of_existing_csv_file()
                if new_file_name == "" : 
                    view.out("Вы ввели имя несуществующего файла, перейти к другой базе заметок не получится.")
                else : 
                    result_of_reading = model.read_data_from_csv(new_file_name)
                    if len(result_of_reading) == 0 : 
                        answer = view.choice_of_two("Данный файл пуст. Вы хотите продолжить с ним работу? ", "1 - Да, хочу", "2 - Нет, не хочу")
                        if answer == 1 : 
                            global_data.data_base_name = new_file_name
                            global_data.int_db_structure = result_of_reading
                            global_data.next_ID = 1
                        else : 
                            print(f"Продолжаем работу с файлом заметок {global_data.data_base_name}")
                    else : 
                        global_data.data_base_name = new_file_name
                        global_data.int_db_structure = result_of_reading
                        print("Вот исходное состояние файла, с которым Вы пожелали работать: \n")
                        print(global_data.int_db_structure)
                        global_data.next_ID = model.get_next_ID(global_data.int_db_structure)
                
            case global_data.QUIT: 
                onward = False

            case _ : 
                view.out("Недопустимая команда. Попробуйте еще раз.")

# Функция запрашивает у пользователя данные для создания заметки: 
# - название
# - текст
def request_note_data() : 
    return view.string_input(global_data.NOTE_NAME_INVIT), view.string_input(global_data.NOTE_BODY_INVIT)






    

    
