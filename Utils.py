import time
import datetime

# Files -------------------------------------------------------------------

path_champlist = './champlist.txt'

path_pick_accuracy = './Accuracy/accuracy_splash.txt'
path_ban_accuracy = './Accuracy/accuracy_icons.txt'

path_auth = './GoogleAuthentication/CSA_secrets_GSuite.json'


# Directories -------------------------------------------------------------

path_splashes = './Assets/Splashes/'
path_splashes_raw = './Assets/Splashes_Raw/'
path_icons = './Assets/Icons/'
path_icons_raw = './Assets/Icons_Raw/'
path_manual_image_overrides = './Assets/Manual_Image_Overrides/'

path_draft_screenshots = './ChampSelectScreenshots/'

path_templates = './Templates/'
path_results = './Results/'


# Champlist ---------------------------------------------------------------

def read_champlist_from_file():
    with open(path_champlist, 'r') as f:
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


# Output

def print_indented(text):
    print(f'{' ' * 24}{text}')
