from datetime import datetime, date, time
from dateutil.parser import parse

try : 
    right_datetime = parse("Лесоповал")
except : 
    print("Невалидная дата")
print(type(right_datetime))
print('right_date = {}'.format(right_datetime))
