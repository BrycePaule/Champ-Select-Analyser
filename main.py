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
    matcher = TemplateMatcher()
    GDI = GoogleDriveInterface()
    cropper = TemplateCropper()

    # Google Sheet output location + increments
    row_inc = 0      # distance from top-left cell of game to game
    col_inc = 5      # distance from top-left cell of game to game

    if len(sys.argv) > 1:
        google_sheet_name = sys.argv[1]
        if sys.argv[2] == 'Game':
            worksheet_name = sys.argv[2] + ' ' + sys.argv[3]
        else:
            worksheet_name = sys.argv[2]
    else:
        google_sheet_name = input('Please enter sheet URL: ')
        worksheet_name = input('Please enter worksheet name: ')

    print(google_sheet_name)
    print(worksheet_name)

    cropper.create_templates()


    for image in cropper.get_champ_select_image():

        # CROPPER

        cropper.create_templates()

        # MATCHER
        print('Matcher working on: ' + image)

        matcher.removePreviousResults()

        picks, bans = matcher.organiseTemplates(cropper.duplicate_count)
        # picks = editTemplates(picks, 'r4.bmp')
        # bans = editTemplates(bans, 'rb3.bmp')

        bans_results = matcher.match(matcher.champlist, bans, cropper.duplicate_count, matcher.icon_path, 'bans')
        picks_results = matcher.match(matcher.champlist, picks, cropper.duplicate_count, matcher.splash_path, 'picks')

        print(' ------------ Bans ------------ ' )
        matcher.printResultsToConsole(bans_results)
        print(' ------------ Picks ------------ ' )
        matcher.printResultsToConsole(picks_results)

        if google_sheet_name != '':
            print('Sending results to Google Sheet ... ')
            GDI.outputToGoogleSheet(bans_results, picks_results, google_sheet_name, worksheet_name)
            GDI.row_start += row_inc
            GDI.col_start += col_inc




    # printUnknownAccuracy('accuracy_splash.txt')
    # printLowAccuracy('accuracy_splash.txt')


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == '-d':
    #         run_scrape_and_scale(download=True)
    # else:
    #     run_scrape_and_scale()

    run_crop_and_match()