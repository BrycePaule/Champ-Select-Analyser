import sys

from Scraper import Scraper
from ImageEditor import ImageEditor
from TemplateMatcher import TemplateMatcher
from GoogleDriveInterface import GoogleDriveInterface
from Utils import start_timer, end_timer



""" CHAMP SELECT ANALYSER"""

def run_scrape_and_scale(download=False):
    time_start = time.perf_counter()

    if download:
        DL = Scraper()
        DL.scrape_champlist()

        for _, name in enumerate(DL.champlist):
            print(f'Downloading   ...   {name}')
            DL.scrape_splash(name, force=False)
            DL.scrape_icon(name, force_scrape=False)

    IEdit = ImageEditor()
    for name in IEdit.champlist:
        print(f'Fixing   ...   {name}')
        IEdit.splash_complete_fix(name)
        IEdit.icon_complete_fix(name)


def run_crop_and_match(duplicate_count=3, match_all=False, spreadsheet_URL=None, worksheet=None):
    if spreadsheet_URL is None:
        spreadsheet_URL = input('Enter spreadsheet URL (enter to skip): ')
        if spreadsheet_URL.isspace() or spreadsheet_URL == '':
            spreadsheet_URL = None

    if worksheet is None:
        worksheet = input('Enter worksheet name (enter to skip): ')
        if worksheet.isspace() or worksheet == '':
            worksheet = None

    time_start = time.perf_counter()

    matcher = TemplateMatcher(duplicate_count)

    for image in matcher.get_champ_select_image(match_all):
        print(f'Working on {image}')
        results = matcher.match(image)
        matcher.print_results(results)

        end_timer(time_start)

        if spreadsheet_URL is not None:
            print('Sending results to Google Sheet ... ')
            GDI = GoogleDriveInterface(spreadsheet_URL, worksheet)
            GDI.output_to_LCK_sheet(results)


def run():

    # Defaults
    _match_all = False
    _spreadsheet_URL = None
    _worksheet_name = None

    # Parse command line args
    if len(sys.argv) >= 2:
        if '-d' in sys.argv or '-download' in sys.argv:
            run_scrape_and_scale(download=True)
        elif '-e' in sys.argv or '-edit' in sys.argv:
            run_scrape_and_scale()

        if '-nm' in sys.argv or '-nomatch' in sys.argv:
            return

        if '-a' in sys.argv or '-all' in sys.argv:
            _match_all = True

            if '-a' in sys.argv:
                sys.argv.remove('-a')
            if '-all' in sys.argv:
                sys.argv.remove('-all')

        if len(sys.argv) >= 3:
            _spreadsheet_URL = sys.argv[1]
            _worksheet_name = sys.argv[2]

            if len(sys.argv) >= 4:
                _worksheet_name = ' '.join(sys.argv[2:])

    run_crop_and_match(
        match_all = _match_all,
        spreadsheet_URL = _spreadsheet_URL,
        worksheet = _worksheet_name,
    )


if __name__ == '__main__':

    timer = start_timer()

    # run()
    run_scrape_and_scale(download=True)

    end_timer(timer)
