import time
import datetime
import sys
import os

from PIL import Image

from Downloader import Downloader
from ImageEditor import ImageEditor
from TemplateMatcher import TemplateMatcher
from GoogleDriveInterface import GoogleDriveInterface
from TemplateCropper import TemplateCropper
from AccuracyManager import AccuracyManager


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


def run_crop_and_match():

    """ GET USER INPUT """
    google_sheet_name, worksheet_name = handle_parameters()

    time_start = time.perf_counter()

    duplicate_count = 3
    match_all = False

    cropper = TemplateCropper(duplicate_count)
    matcher = TemplateMatcher(duplicate_count)
    GDI = GoogleDriveInterface()

    # Google Sheet output location + increments
    row_inc = 0      # distance from top-left cell of game to game
    col_inc = 5      # distance from top-left cell of game to game


    for image in cropper.get_champ_select_image():
        print(f'Working on {image}')

        cropper.create_templates()
        picks, bans = matcher.organise_templates()


        bans_results = matcher.match(bans, bans=True)
        picks_results = matcher.match(picks)

        matcher.print_results(bans_results)
        matcher.print_results(picks_results)


        end_timer(time_start)

        if len(google_sheet_name) >= 10:
            print('Sending results to Google Sheet ... ')
            GDI.output_to_spreadsheet(bans_results, picks_results, google_sheet_name, worksheet_name)
            GDI.row_start += row_inc
            GDI.col_start += col_inc


def handle_parameters():
    if len(sys.argv) > 1:
        google_sheet_name = sys.argv[1]
        if sys.argv[2] == 'Game':
            worksheet_name = sys.argv[2] + ' ' + sys.argv[3]
        else:
            worksheet_name = sys.argv[2]
    else:
        google_sheet_name = input('Enter spreadsheet URL: ')
        worksheet_name = input('Enter worksheet name: ')

    return google_sheet_name, worksheet_name


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == '-d':
    #         run_scrape_and_scale(download=True)
    # else:
    #     run_scrape_and_scale()

    run_crop_and_match()