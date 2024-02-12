from datetime import datetime, date, time
from dateutil.parser import parse

try : 
    right_datetime = parse("2025-02-28")
except : 
    print("Невалидная дата")
print('right_date = {}'.format(right_datetime))
