"""

    FROM STOCK-SCRAPER

"""

import os
import pickle
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


URL = 'https://www.fnarena.com/index.php?s='
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
stock_list_sheet_id = '1VgeoxM-5hwr7Y4V5KIJgDU-jAyolIMX3juzeOpuRw2w'
stock_list_range = 'Stocks!A2:A'

def get_oauth2_authentication_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def fetch_stock_list(creds):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=stock_list_sheet_id,
        range=stock_list_range).execute()

    return [stock.lower() for row in result.get('values', []) for stock in row]
