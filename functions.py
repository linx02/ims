from product_model import *
import print_output
import re
from setup import *

def update_stock(sales=None, scraps=None, inventory_list=None):
    cols = 'ABCDEF'

    def update_qty(list_to_use):
        for product in list_to_use:
            cell = stock_worksheet.find(product[0])
            qty_cell = stock_worksheet.cell(cell.row, cell.col - 1)

            index = cols[cell.col - 2]
            stock_worksheet.update(f'{index}{cell.row}', int(qty_cell.value) - int(product[1]))
    
    if sales != None: update_qty(sales)
    if scraps != None: update_qty(scraps)

#Worksheet.update(value = [[]], range_name=)' arguments 'range_name' and 'values' will swap, values will be mandatory of type: 'list(list(...))'

def update():
    sales = sales_worksheet.get_all_values()[1:]
    scraps = scrap_worksheet.get_all_values()[1:]

    update_stock(sales=sales, scraps=scraps)

    for item in sales:
        item[1] = int(item[1])
    
    for item in scraps:
        item[1] = int(item[1])

    data = {
        "date" : str(datetime.now().date()),
        "sold" : sales,
        "scrap" : scraps
    }

    sales_history.append(data)

    with open('test_history.json', 'w') as json_file:
        json.dump(sales_history, json_file)

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
    print_output.print_dataof(product)

def scrap():
    to_scrap = []
    while True:
        gtin = input('Enter product gtin to scrap: ')

        if "apply" in gtin: break

        qty = input('Enter quantity: ')

        to_scrap.append([gtin, qty])
    
    for row in to_scrap:
        scrap_worksheet.append_row(row)


def help(command):
    pass

def execute_cmd(command):
    pattern = r"\b\d+\b"
    gtin = lambda: re.search(pattern, command).group()

    try:
        if 'update' in command:
            update()
        elif 'updateinv' in command:
            pass
        elif 'priceof' in command:
            priceof(gtin())
        elif 'instock' in command:
            instock(gtin())
        elif 'dataof' in command:
            dataof(gtin())
        elif 'scrap' in command:
            scrap()
        elif 'help' in command:
            pass
        elif 'exit' in command:
            exit()
        else:
            print(f'No such command: "{command}"')
    except SyntaxError as e:
        print(f'Invalid usage of ({command}): {e}\n')
        print(f'Please type "help {command}" to see correct usage.\n')