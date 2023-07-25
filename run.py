import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock')

stock = SHEET.worksheet('full_stock')

def print_main():
    print(
"""
*----------------*
|   YourStore    |
|     IMS        |
*----------------*
| Commands:      |
|                |
| updatesales    |
| updateinv      |
| priceof [GTIN] |
| instock [GTIN] |
| dataof [GTIN]  |
| scrap          |
| help [COMMAND] |
*----------------*
"""
)

def updatesales():
    pass

def updateinv():
    pass

def priceof(gtin):
    pass

def instock(gtin):
    pass

def dataof(gtin):
    pass

def scrap():
    pass

def help(command):
    pass

def execute_cmd(command):
    pass

def main():
    print_main()
    command = input('YourStore > ')
    execute_cmd(command)

main()