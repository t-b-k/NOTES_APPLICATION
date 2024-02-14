from datetime import datetime, date, time
from dateutil.parser import parse

try : 
    right_datetime = parse("2024-04-30")
    print(type(right_datetime))
    print('right_date = {}'.format(right_datetime))
except : 
    print("Невалидная дата")