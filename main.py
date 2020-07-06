import time
import datetime
import sys

from contextlib import suppress

from Downloader import Downloader
from ImageEditor import ImageEditor
from TemplateMatcher import TemplateMatcher
from GoogleDriveInterface import GoogleDriveInterface


""" TIMERS """

def start_timer():
    return time.perf_counter()


def end_timer(time_start):
    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))

    print('\n-----------------------')
    print(f'Runtime: {elapsed_time}')
    print('-----------------------')


""" CHAMP SELECT ANALYSER"""

def run_scrape_and_scale(download=False):
    time_start = time.perf_counter()

    if download:
        DL = Downloader()
        DL.scrape_champlist_raw()
        DL.convert_champlist_to_save()
        DL.convert_champlist_to_splash()
        DL.convert_champlist_to_icon()

        for index, name in enumerate(DL.champlist_save):
            print(f'Downloading   ...   {name}')
            DL.scrape_splash(DL.champlist_splash[index])
            DL.scrape_icon(DL.champlist_icon[index])

    IEdit = ImageEditor()
    for name in IEdit.champlist:
        print(f'Fixing   ...   {name}')
        IEdit.splash_complete_fix(name)
        IEdit.icon_complete_fix(name)

    end_timer(time_start)


def run_crop_and_match(duplicate_count=3, match_all=False, spreadsheet_URL=None, worksheet=None):

    if spreadsheet_URL is None:
        spreadsheet_URL = input('Enter spreadsheet URL (enter to skip): ')

    if worksheet is None:
        worksheet = input('Enter worksheet name (enter to skip): ')

    time_start = time.perf_counter()

    GDI = GoogleDriveInterface(spreadsheet_URL, worksheet)
    matcher = TemplateMatcher(duplicate_count)
    ban_results, pick_results = matcher.analyse_champion_select(match_all)

    end_timer(time_start)

    if spreadsheet_URL is not None:
        print('Sending results to Google Sheet ... ')
        GDI.output_to_spreadsheet(ban_results, pick_results)


def handle_parameters():

    match_all = False
    spreadsheet_URL = None
    worksheet_name = None

    if len(sys.argv) >= 2:
        if '-d' in sys.argv or '-download' in sys.argv:
            run_scrape_and_scale(download=True)
        elif '-e' in sys.argv or '-edit' in sys.argv:
            run_scrape_and_scale()

        if '-nm' in sys.argv or '-nomatch' in sys.argv:
            return

        if '-a' in sys.argv or '-all' in sys.argv:
            match_all = True

            if '-a' in sys.argv:
                sys.argv.remove('-a')
            if '-all' in sys.argv:
                sys.argv.remove('-all')

        if len(sys.argv) >= 3:
            spreadsheet_URL = sys.argv[1]
            worksheet_name = sys.argv[2]

            if len(sys.argv) >= 4:
                worksheet_name = ' '.join(sys.argv[2:])

    run_crop_and_match(
        match_all=match_all,
        spreadsheet_URL=spreadsheet_URL,
        worksheet=worksheet_name
    )

if __name__ == '__main__':

    handle_parameters()