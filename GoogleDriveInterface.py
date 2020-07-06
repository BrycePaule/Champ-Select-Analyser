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


    def output_to_spreadsheet(self, ban_results, pick_results):
        """
        Authorises, and connects to given google sheet.  Prints TemplateMatcher
        results to the given location on the sheet
        """

        client = gspread.authorize(self.creds)
        sheet = client.open_by_url(self.google_sheet_url).worksheet(self.worksheet)

        row = self.row_start
        col = self.col_start

        sheet.update_cell(row, col, (ban_results[0][1]))
        sheet.update_cell(row + 1, col, (ban_results[1][1]))
        sheet.update_cell(row + 2, col, (ban_results[2][1]))
        sheet.update_cell(row + 3, col, (ban_results[3][1]))
        sheet.update_cell(row + 4, col, (ban_results[4][1]))

        sheet.update_cell(row, col + 1, (pick_results[0][1]))
        sheet.update_cell(row + 1, col + 1, (pick_results[1][1]))
        sheet.update_cell(row + 2, col + 1, (pick_results[2][1]))
        sheet.update_cell(row + 3, col + 1, (pick_results[3][1]))
        sheet.update_cell(row + 4, col + 1, (pick_results[4][1]))

        sheet.update_cell(row, col + 2, (pick_results[5][1]))
        sheet.update_cell(row + 1, col + 2, (pick_results[6][1]))
        sheet.update_cell(row + 2, col + 2, (pick_results[7][1]))
        sheet.update_cell(row + 3, col + 2, (pick_results[8][1]))
        sheet.update_cell(row + 4, col + 2, (pick_results[9][1]))

        sheet.update_cell(row, col + 3, (ban_results[5][1]))
        sheet.update_cell(row + 1, col + 3, (ban_results[6][1]))
        sheet.update_cell(row + 2, col + 3, (ban_results[7][1]))
        sheet.update_cell(row + 3, col + 3, (ban_results[8][1]))
        sheet.update_cell(row + 4, col + 3, (ban_results[9][1]))

        self.row_start += self.row_increment
        self.col_start += self.col_increment