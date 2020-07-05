import time
import datetime

from Downloader import Downloader


def run():
    DL = Downloader()

    champlist_for_splash_download = DL.scrapeChamplist()
    champlist = DL.fixAndExportChamplist(champlist_for_splash_download)
    champlist_for_icon_download = DL.fixChamplistForIconDownload(champlist)

    DL.scrapeSplashes(champlist_for_splash_download, True)
    DL.scrapeIcons(champlist_for_icon_download, True)


if __name__ == '__main__':
    time_start = time.perf_counter()

    run()

    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))
    print()
    print('Runtime: ' + elapsed_time)


