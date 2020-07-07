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

        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_url(self.google_sheet_url).worksheet(self.worksheet)


    def output_to_spreadsheet(self, ban_results, pick_results):
        """ Outputs results to google sheet in __init__ method. """

        row = self.row_start
        col = self.col_start

        self.sheet.update_cell(row, col, (ban_results[0][1]))
        self.sheet.update_cell(row + 1, col, (ban_results[1][1]))
        self.sheet.update_cell(row + 2, col, (ban_results[2][1]))
        self.sheet.update_cell(row + 3, col, (ban_results[3][1]))
        self.sheet.update_cell(row + 4, col, (ban_results[4][1]))

        self.sheet.update_cell(row, col + 1, (pick_results[0][1]))
        self.sheet.update_cell(row + 1, col + 1, (pick_results[1][1]))
        self.sheet.update_cell(row + 2, col + 1, (pick_results[2][1]))
        self.sheet.update_cell(row + 3, col + 1, (pick_results[3][1]))
        self.sheet.update_cell(row + 4, col + 1, (pick_results[4][1]))

        self.sheet.update_cell(row, col + 2, (pick_results[5][1]))
        self.sheet.update_cell(row + 1, col + 2, (pick_results[6][1]))
        self.sheet.update_cell(row + 2, col + 2, (pick_results[7][1]))
        self.sheet.update_cell(row + 3, col + 2, (pick_results[8][1]))
        self.sheet.update_cell(row + 4, col + 2, (pick_results[9][1]))

        self.sheet.update_cell(row, col + 3, (ban_results[5][1]))
        self.sheet.update_cell(row + 1, col + 3, (ban_results[6][1]))
        self.sheet.update_cell(row + 2, col + 3, (ban_results[7][1]))
        self.sheet.update_cell(row + 3, col + 3, (ban_results[8][1]))
        self.sheet.update_cell(row + 4, col + 3, (ban_results[9][1]))

        self.row_start += self.row_increment
        self.col_start += self.col_increment


    def output_to_LCK_sheet(self, ban_results, pick_results):
        """ Specific output to LCK Notes style spreadsheet """

        blue_bans = [[champ_name] for (_, champ_name, _) in ban_results[:5]]
        blue_picks = [[champ_name] for (_, champ_name, _) in pick_results[:5]]
        red_bans = [[champ_name] for (_, champ_name, _) in ban_results[:5]]
        red_picks = [[champ_name] for (_, champ_name, _) in pick_results[:5]]

        self.sheet.update('M23:M27', blue_bans)
        self.sheet.update('N23:N27', blue_picks)
        self.sheet.update('O23:O27', red_bans)
        self.sheet.update('P23:P27', red_picks)