import os
import sys
import Utils

from Scraper import Scraper
from ImageEditor import ImageEditor
from TemplateMatcher import TemplateMatcher
from GoogleDriveInterface import GoogleDriveInterface


def scrape_images(force_scrape=False):
    scraper = Scraper()
    scraper.scrape_champlist()

    for name in scraper.champlist:
        print(f'Downloading   ...   {name}')
        scraper.scrape_champ_splashes(name, force_scrape)
        scraper.scrape_champ_icons(name, force_scrape)

def optimise_scraped_images():
    editor = ImageEditor()

    for name in editor.champlist:
        print(f'Fixing   ...   {name}')
        editor.optimise_splashes(name)
        editor.optimise_icons(name)

def parse_screenshots(resize_attempts_before_skip=5, match_all=False):

    # ===================================================================================
    # No longer have access to the google sheet, likely obsolete and won't be re-used

    # Remote save info
    # spreadsheet_URL = input('Enter spreadsheet URL (enter to skip): ').strip()
    # worksheet_name = input('Enter worksheet name (enter to skip): ').strip()
    # ===================================================================================

    # Run image parser
    matcher = TemplateMatcher(resize_attempts_before_skip)

    for draft_filename in matcher.get_draft_screenshot(match_all):
        print(f'Matching {draft_filename}')
        results = matcher.parse(draft_filename)
        matcher.print_results(results)

        # if spreadsheet_URL:
        #     print('Sending results to Google Sheet ... ')
        #     GDI = GoogleDriveInterface(spreadsheet_URL, worksheet_name)
        #     GDI.output_to_LCK_sheet(results)


def run():
    # Default settings
    _run_scraper = False
    _force_scrape = False

    _optimise_scraped_images = False

    _run_matcher = True
    _match_all = False

    # Parse command line args
    for arg in sys.argv:
        if arg == '-s' or arg == '-scrape':
            _run_scraper = True

        if arg == '-fs' or arg == '-force_scrape':
            _run_scraper = True
            _force_scrape = True

        if arg == '-o' or arg == '-optimise':
            _optimise_scraped_images = True

        if arg == '-np' or arg == '-no_parse':
            _run_matcher = False

        if arg == '-a' or arg == '-all':
            _run_matcher = True
            _match_all = True


    # Create required directories
    os.makedirs(Utils.path_splashes, exist_ok=True)
    os.makedirs(Utils.path_splashes_raw, exist_ok=True)
    os.makedirs(Utils.path_icons, exist_ok=True)
    os.makedirs(Utils.path_icons_raw, exist_ok=True)

    os.makedirs(Utils.path_manual_image_overrides, exist_ok=True)
    os.makedirs(Utils.path_draft_screenshots, exist_ok=True)

    os.makedirs(Utils.path_templates, exist_ok=True)
    os.makedirs(Utils.path_results, exist_ok=True)


    # Run app
    if _run_scraper:
        scrape_images(_force_scrape)

    if _optimise_scraped_images:
        optimise_scraped_images()

    if _run_matcher:
        parse_screenshots(match_all=_match_all)


if __name__ == '__main__':
    timer = Utils.start_timer()
    run()
    Utils.end_timer(timer)
