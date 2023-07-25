import gspread
from google.oauth2.service_account import Credentials
import re

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
stock_data = stock.get_all_values()

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
    for product in stock_data:
        if gtin == product[-1]:
            return f'{product[0]}: ${product[1][1:]}'
    return f'No match for GTIN: {gtin}'

def instock(gtin):
    pass

def dataof(gtin):
    pass

def scrap():
    pass

def help(command):
    pass

def execute_cmd(command):
    pattern = r"\b\d+\b"
    gtin = re.search(pattern, command).group()

    if 'updatesales' in command:
        pass
    if 'updateinv' in command:
        pass
    if 'priceof' in command:
        print(priceof(gtin))
    if 'instock' in command:
        pass
    if 'dataof' in command:
        pass
    if 'scrap' in command:
        pass
    if 'help' in command:
        pass
    if 'exit' in command:
        exit()

def main():
    print_main()
    while True:
        command = input('YourStore > ')
        execute_cmd(command)

main()