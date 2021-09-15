import gspread
from google.oauth2.service_account import Credentials
import finnhub
import finnhubkey

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("portfolio-tracker")
FINNHUB_CLIENT = finnhub.Client(api_key=finnhubkey.key)

print(FINNHUB_CLIENT.aggregate_indicator('AAPL', 'D'))