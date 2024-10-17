import gspread
import Utils

from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveInterface:

    """ Handles sending TemplateMatcher results to the given google sheet """

    def __init__(self, google_sheet_url, worksheet):
        self.credential_file = Utils.path_auth
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credential_file, self.scope)

        self.google_sheet_url = google_sheet_url
        self.worksheet = worksheet

        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_url(self.google_sheet_url).worksheet(self.worksheet)


    def output_to_LCK_sheet(self, results):
        """ Specific output to LCK Notes style spreadsheet """
        results_list = list(results.values())

        blue_bans = [[champion] for champion, accuracy in results_list[:5]]
        red_bans = [[champion] for champion, accuracy in results_list[5:10]]
        blue_picks = [[champion] for champion, accuracy in results_list[10:15]]
        red_picks = [[champion] for champion, accuracy in results_list[15:]]

        self.sheet.update('M23:M27', blue_bans)
        self.sheet.update('N23:N27', blue_picks)
        self.sheet.update('O23:O27', red_picks)
        self.sheet.update('P23:P27', red_bans)
