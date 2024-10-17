import time
import datetime

# Files -------------------------------------------------------------------

path_champlist = './Inputs/champlist.txt'

path_pick_accuracy = './Outputs/Accuracy/accuracy_splash.txt'
path_ban_accuracy = './Outputs/Accuracy/accuracy_icons.txt'

path_auth = './GoogleAuthentication/CSA_secrets_GSuite.json'


# Directories -------------------------------------------------------------

path_splashes = './Inputs/Splashes/'
path_splashes_raw = './Inputs/Splashes_Raw/'
path_icons = './Inputs/Icons/'
path_icons_raw = './Inputs/Icons_Raw/'

path_manual_image_overrides = './Inputs/Manual_Image_Overrides/'
path_draft_screenshots = './Inputs/Champ_Select_Screenshots/'

path_templates = './Outputs/Templates/'
path_results = './Outputs/Results/'

path_readme_images = './Readme/'


# Champlist ---------------------------------------------------------------

def read_champlist_from_file():
    with open(path_champlist, 'r') as f:
        return [name.strip() for name in f]


# Timing ------------------------------------------------------------------

def start_timer():
    return time.perf_counter()


def end_timer(time_start):
    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=round(time_stop - time_start)))

    print('\n')
    print('--------------------------------')
    print(f'Runtime: {elapsed_time}')
    print('--------------------------------')


# Output

def print_indented(text):
    print(f'{' ' * 24}{text}')
