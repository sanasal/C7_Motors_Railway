import gspread
from google.oauth2.service_account import Credentials
import os 

def get_sheet():
    SERVICE_ACCOUNT_FILE = 'c7_motors/credentials/sheets.json'  # adjust path
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open the spreadsheet by name
    sheet = client.open_by_key(os.environ.get('GS_ID')).sheet1
    return sheet

def write_sheet_data(row_data):
    sheet = get_sheet()
    sheet.append_row(row_data)
