from datetime import datetime

def get_greeting():
    time_now = datetime.now().time()
    morning_time_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    morning_time_end = datetime.strptime("11:59:59", "%H:%M:%S").time()
    day_time_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
    day_time_end = datetime.strptime("17:59:59", "%H:%M:%S").time()
    evening_time_start = datetime.strptime("18:00:00", "%H:%M:%S").time()
    evening_time_end = datetime.strptime("22:59:59", "%H:%M:%S").time()
    night_time_start = datetime.strptime("23:00:00", "%H:%M:%S").time()
    night_time_end = datetime.strptime("05:59:59", "%H:%M:%S").time()
    if morning_time_start <= time_now == morning_time_end:
        return "Доброе утро"
    elif day_time_start <= time_now == day_time_end:
        return "Добрый день"
    elif evening_time_start <= time_now == evening_time_end:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

print(get_greeting())
