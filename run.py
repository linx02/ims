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
            data = f'{self.supplier}'
        if info == 'qty':
            data = f'{self.qty}'
        if info == 'gtin':
            data = f'{self.gtin}'
        
        return f'{self.name}: {data}'
    
    def sold_items(self, time_period=None):
        if type(time_period) == int:
            current_date = datetime.now().date()
            date_list = [current_date - timedelta(days=i) for i in range(time_period)]

        else:
            start_datetime = time_period[0]
            end_datetime = time_period[1]

            date_list = [start_datetime + timedelta(days=i) for i in range((end_datetime - start_datetime).days + 1)]

        sold_items = []

        for date in date_list:
            for item in sales_history:
                if item["date"] == str(date):
                    for product in item["sold"]:
                        if product[0] == self.gtin:
                            sold_items.append(product)
        
        total = 0
        for item in sold_items:
            total += item[1]
        
        return total
    
    def compare_sales(self, time_period):
        current_date = datetime.now().date()
        delta = timedelta(days=time_period)
        last_datetime = datetime(current_date.year - 1, current_date.month, current_date.day)
        last_datetime_start = last_datetime - delta
        last_date = last_datetime.date()
        last_date_start = last_datetime_start.date()

        current_date_str = current_date.strftime('%Y-%m-%d')
        last_date_str = last_date.strftime('%Y-%m-%d')
        last_date_start_str = last_date_start.strftime('%Y-%m-%d')

        last_sales = self.sold_items(time_period=[last_date_start, last_date])
        current_sales = self.sold_items(time_period)

        return current_sales - last_sales


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
Sold(7 days): {product.sold_items(7)}
-------------
Sold(30 days): {product.sold_items(30)}
--------------
+ / - (7 days): {product.compare_sales(7)}
---------------
+ / - (30 days): {product.compare_sales(30)}
----------------
"""
    )

def scrap():
    pass

def help(command):
    pass

def execute_cmd(command):
    pattern = r"\b\d+\b"
    gtin = lambda: re.search(pattern, command).group()

    try:
        if 'updatesales' in command:
            pass
        elif 'updateinv' in command:
            pass
        elif 'priceof' in command:
            priceof(gtin())
        elif 'instock' in command:
            instock(gtin())
        elif 'dataof' in command:
            dataof(gtin())
        elif 'scrap' in command:
            pass
        elif 'help' in command:
            pass
        elif 'exit' in command:
            exit()
        else:
            print(f'No such command: "{command}"')
    except Exception as e:
        print(f'Invalid usage of ({command}): {e}\n')
        print(f'Please type "help {command}" to see correct usage.\n')

def main():
    print_main()
    while True:
        command = input('YourStore > ')
        execute_cmd(command)

main()

#1275660192613