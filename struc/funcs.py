from datetime import datetime

def get_cur_time():
    raw_time = datetime.now()
    formatted_time = raw_time.strftime("%d-%m-%Y--%H-%M-%S")
    return formatted_time