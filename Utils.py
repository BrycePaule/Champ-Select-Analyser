import time
import datetime


# Champlist ---------------------------------------------------------------

def get_champlist_as_list():
    with open('./champlist.txt', 'r') as f:
        return [name.strip() for name in f]


# Timing ------------------------------------------------------------------

def start_timer():
    return time.perf_counter()


def end_timer(time_start):
    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))

    print('\n-----------------------')
    print(f'Runtime: {elapsed_time}')
    print('-----------------------')