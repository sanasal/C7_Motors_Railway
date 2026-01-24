import os
import base64
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def ensure_credentials_file():
    creds_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")
    path = "ghaith_project/credentials/sheets.json"

    if creds_b64 and not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(base64.b64decode(creds_b64))

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


def get_sheet():
    ensure_credentials_file()

    SERVICE_ACCOUNT_FILE = 'ghaith_project/credentials/sheets.json'
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.Client(auth=creds)
    client.login()   # authenticate with the creds

    sheet = client.open_by_key(os.environ.get('GS_ID')).sheet1
    return sheet


def write_sheet_data(row_data):
    sheet = get_sheet()
    sheet.append_row(row_data)
