import gspread
from google.oauth2.service_account import Credentials
import re
import json
from datetime import datetime, timedelta

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock')

# Load stock data
stock = SHEET.worksheet('full_stock')
stock_data = stock.get_all_values()

# Load sales history data
with open('sales_history.json', 'r') as f:
    sales_history = json.load(f)

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

class Product:

    def __init__(self, gtin):
        global stock_data
        global sales_history
        for product in stock_data:
            if gtin == product[-1]:
                self.name = product[0]
                self.price = product[1]
                self.supplier_price = product[2]
                self.supplier = product[3]
                self.qty = product[4]
                self.gtin = gtin
    
    def get(self, info):
        data = None
        if info == 'price':
            data = f'${self.price[1:]}'
        if info == 'supplier_price':
            data = f'${self.supplier_price[1:]}'
        if info == 'supplier':
            data = f'${self.supplier}'
        if info == 'qty':
            data = f'${self.qty}'
        if info == 'gtin':
            data = f'${self.gtin}'
        
        return f'{self.name}: {data}'
    
    def compare_sales(self, days_num):
        current_date = datetime.now().date()
        date_list = [current_date - timedelta(days=i) for i in range(days_num)]

        sold_items = []

        for date in date_list:
            for item in sales_history:
                if item["date"] == date:
                    for product in item["sold"]:
                        if product[0] == self.name:
                            sold_items.append(product)
        
        return(sold_items)



def updatesales():
    pass

def updateinv():
    pass

def priceof(gtin):
    product = Product(gtin)
    print(product.get('price'))

def instock(gtin):
    product = Product(gtin)
    print(product.get('qty'))

def dataof(gtin):
    product = Product(gtin)
    print(
f"""
Name: {product.name}
-----
Price: {product.price}
------
SupplierPrice: {product.supplier_price}
--------------
Supplier: {product.supplier}
---------
Qty in stock: {product.qty}
-------------
Sold(7 days): {product.compare_sales(30)}
-------------
Sold(30 days):
--------------
Sold(365 days):
---------------
+ / - (7 days):
---------------
+ / - (30 days):
----------------
Scrap(7 days):
--------------
Scrap(30 days):
---------------
"""
    )

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
        priceof(gtin)
    if 'instock' in command:
        instock(gtin)
    if 'dataof' in command:
        dataof(gtin)
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

#1275660192613