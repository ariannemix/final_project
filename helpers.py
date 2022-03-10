import time


def get_time():
    time_tuple = time.localtime()
    time_list = list(time_tuple[slice(0, 3)])
    for i in range(0, 3):
        if time_list[i] < 10:
            time_list[i] = f"0{time_list[i]}"
    formatted_string = f"{time_list[0]}-{time_list[1]}-{time_list[2]}"
    return formatted_string
