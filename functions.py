from product_model import *
import print_output
import re
from setup import *

def update_stock(sales=None, scraps=None, inventory_list=None):
    print_output.print_loading('update_stock')

    cols = 'ABCDEF'

    def update_qty(list_to_use):
        for product in list_to_use:
            cell = stock_worksheet.find(product[0])
            qty_cell = stock_worksheet.cell(cell.row, cell.col - 1)

            index = cols[cell.col - 2]
            stock_worksheet.update(f'{index}{cell.row}', int(qty_cell.value) - int(product[1]))
    
    if sales != None: update_qty(sales)
    if scraps != None: update_qty(scraps)

    if inventory_list != None:
        for product in inventory_list:
            cell = stock_worksheet.find(product[0])

            index = cols[cell.col - 2]
            stock_worksheet.update(f'{index}{cell.row}', int(product[1]))
    

#Worksheet.update(value = [[]], range_name=)' arguments 'range_name' and 'values' will swap, values will be mandatory of type: 'list(list(...))'

def update():
    confirm = input('Are you sure you want to update? This means overwriting your current stock and history data. (y/n)')

    if confirm == 'y':
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

        print_output.print_loading('update_history')
        with open('sales_history.json', 'w') as json_file:
            json.dump(sales_history, json_file)
    
    elif confirm == 'n':
        return
    else:
        update()
    
    reload_data()

def updateinv():
    confirm = input('Are you sure you want to update? This means overwriting your current stock and history data. (y/n)')
    if confirm == 'y':
        inventory = inv_worksheet.get_all_values()[1:]
        update_stock(inventory_list=inventory)
    elif confirm == 'n':
        return
    else:
        updateinv()
    
    reload_data()

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

        to_scrap.append([gtin, int(qty)])
    
    for row in to_scrap:
        scrap_worksheet.append_row(row)


def help(command):
    print_output.print_help(command)

def execute_cmd(command):
    entire_command = command
    pattern = r"\b\d+\b"
    gtin = lambda: re.search(pattern, entire_command).group()
    
    try:
        if 'update' == command:
            update()
        elif 'updateinv' == command:
            updateinv()
        elif 'priceof' == command[:len('priceof')]:
            command = 'priceof'
            priceof(gtin())
        elif 'instock' == command[:len('instock')]:
            command = 'instock'
            instock(gtin())
        elif 'dataof' == command[:len('dataof')]:
            command = 'dataof'
            dataof(gtin())
        elif 'scrap' == command:
            scrap()
        elif 'help' == command[:len('help')]:
            command = 'help'
            help(command[5:])
        elif 'exit' == command:
            exit()
        else:
            print(f'No such command: "{command}"')
    except SyntaxError as e:
        print(f'Invalid usage of ({command}): {e}\n')
        print(f'Please type "help {command}" to see correct usage.\n')