import json
from google.oauth2.service_account import Credentials
import gspread

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock')
stock_worksheet = SHEET.worksheet('full_stock')
sales_worksheet = SHEET.worksheet('today_sales')
scrap_worksheet = SHEET.worksheet('today_scrap')
inv_worksheet = SHEET.worksheet('inventory')

# Load stock data
stock = SHEET.worksheet('full_stock')
stock_data = stock.get_all_values()

# Load sales history data
with open('sales_history.json', 'r') as f:
    sales_history = json.load(f)
