import time
import datetime

from Downloader import Downloader


def run():
    DL = Downloader()

    champlist_for_splash_download = DL.scrape_champlist_raw()
    champlist = DL.get_champlist_for_saving(champlist_for_splash_download)
    champlist_for_icon_download = DL.get_champlist_for_icon_download(champlist)

    DL.scrape_splashes(champlist_for_splash_download, True)
    DL.scrape_icons(champlist_for_icon_download, True)


if __name__ == '__main__':
    time_start = time.perf_counter()

    run()

    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))
    print()
    print('Runtime: ' + elapsed_time)


