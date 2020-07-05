import time
import datetime
import sys

from Downloader import Downloader
from ImageEditor import ImageEditor

from TemplateMatcher import TemplateMatcher
from GoogleDriveInterface import GoogleDriveInterface
from ImageCropper import ImageCropper


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
    cropper = ImageCropper()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            run_scrape_and_scale(download=True)
    else:
        run_scrape_and_scale()


