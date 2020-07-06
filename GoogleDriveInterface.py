import gspread

from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveInterface():

    """ Handles sending TemplateMatcher results to the given google sheet """

    def __init__(self, google_sheet_url, worksheet):
        self.credential_file = 'GoogleAuthentication/CSA_secrets_GSuite.json'
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credential_file, self.scope)

        self.google_sheet_url = google_sheet_url
        self.worksheet = worksheet

        self.row_start = 23
        self.col_start = 13

        self.row_increment = 0
        self.col_increment = 5


    def output_to_spreadsheet(self, bans_results, picks_results):
        """
        Authorises, and connects to given google sheet.  Prints TemplateMatcher
        results to the given location on the sheet
        """

        client = gspread.authorize(self.creds)
        sheet = client.open_by_url(self.google_sheet_url).worksheet(self.worksheet)

        row = self.row_start
        col = self.col_start

        sheet.update_cell(row, col, (bans_results[0].split(' - '))[1])
        sheet.update_cell(row + 1, col, (bans_results[1].split(' - '))[1])
        sheet.update_cell(row + 2, col, (bans_results[2].split(' - '))[1])
        sheet.update_cell(row + 3, col, (bans_results[3].split(' - '))[1])
        sheet.update_cell(row + 4, col, (bans_results[4].split(' - '))[1])

        sheet.update_cell(row, col + 1, (picks_results[0].split(' - '))[1])
        sheet.update_cell(row + 1, col + 1, (picks_results[1].split(' - '))[1])
        sheet.update_cell(row + 2, col + 1, (picks_results[2].split(' - '))[1])
        sheet.update_cell(row + 3, col + 1, (picks_results[3].split(' - '))[1])
        sheet.update_cell(row + 4, col + 1, (picks_results[4].split(' - '))[1])

        sheet.update_cell(row, col + 2, (picks_results[5].split(' - '))[1])
        sheet.update_cell(row + 1, col + 2, (picks_results[6].split(' - '))[1])
        sheet.update_cell(row + 2, col + 2, (picks_results[7].split(' - '))[1])
        sheet.update_cell(row + 3, col + 2, (picks_results[8].split(' - '))[1])
        sheet.update_cell(row + 4, col + 2, (picks_results[9].split(' - '))[1])

        sheet.update_cell(row, col + 3, (bans_results[5].split(' - '))[1])
        sheet.update_cell(row + 1, col + 3, (bans_results[6].split(' - '))[1])
        sheet.update_cell(row + 2, col + 3, (bans_results[7].split(' - '))[1])
        sheet.update_cell(row + 3, col + 3, (bans_results[8].split(' - '))[1])
        sheet.update_cell(row + 4, col + 3, (bans_results[9].split(' - '))[1])

        self.row_start += self.row_increment
        self.col_start += self.col_increment