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
    global data_base
    view.out(INIT_MESSAGE, data_base)

    
