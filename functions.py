from product_model import *
import print_output
from setup import *

def gtin_exists(gtin):
    global stock_data
    for row in stock_data:
        if str(gtin) == row[-1]: return True

def validate_data(*args):
    errors = False
    def validate(worksheet):
        nonlocal errors
        for row_index, item in enumerate(worksheet):
            if len(item) > 3:
                print_output.print_error('invalid_data', row=row_index + 1)
                errors = True
                continue
            if item[0] not in existing_gtins:
                print_output.print_error('invalid_data', row=row_index + 1)
                errors = True
                continue
            try:
                int(item[0])
                int(item[1])
            except Exception as e:
                print_output.print_error('invalid_data', row=row_index + 1)
                errors = True
        

    if 'sales' in args: validate(sales_worksheet.get_all_values()[1:])
    if 'scraps' in args: validate(scrap_worksheet.get_all_values()[1:])
    if 'inventory' in args: validate(inv_worksheet.get_all_values()[1:])
    
    return errors


def update_stock(sales=None, scraps=None, inventory_list=None):
    print_output.print_loading('update_stock')

    cols = 'ABCDEF'

    def update_qty(list_to_use):
        for product in list_to_use:
            cell = stock_worksheet.find(product[0])
            qty_cell = stock_worksheet.cell(cell.row, cell.col - 1)

            index = cols[cell.col - 2]
            try:
                stock_worksheet.update(f'{index}{cell.row}', int(qty_cell.value) - int(product[1]))
            except Exception as e:
                print_output.print_error('invalid_data', cell.row)
                print('Please resolve errors before updating')
                return True
    
    if sales != None: errors = update_qty(sales)
    if errors: return True
    if scraps != None: errors = update_qty(scraps)
    if errors: return True

    if inventory_list != None:
        for product in inventory_list:
            cell = stock_worksheet.find(product[0])

            index = cols[cell.col - 2]
            stock_worksheet.update(f'{index}{cell.row}', int(product[1]))
    

#Worksheet.update(value = [[]], range_name=)' arguments 'range_name' and 'values' will swap, values will be mandatory of type: 'list(list(...))'

def update():
    confirm = input('Are you sure you want to update? This means overwriting your current stock and history data. (y/n) ')
    confirm_overwrite = 'n'

    if sales_history[-1]["date"] == str(datetime.now().date()):
        confirm_overwrite = input('Todays date already exists in the sales history. Are you sure you want to overwrite it? (y/n) ')

    if confirm == 'y' and confirm_overwrite == 'y':

        errors = validate_data('sales', 'scraps')

        if errors:
            print('Please resolve errors before updating data')
            return

        sales = sales_worksheet.get_all_values()[1:]
        scraps = scrap_worksheet.get_all_values()[1:]

        errors = update_stock(sales=sales, scraps=scraps)
        if errors: return

        for item in sales:
            item[1] = int(item[1])
        
        for item in scraps:
            item[1] = int(item[1])

        data = {
            "date" : str(datetime.now().date()),
            "sold" : sales,
            "scrap" : scraps
        }

        if confirm_overwrite == 'y':
            sales_history[-1] = data
        else:
            sales_history.append(data)

        print_output.print_loading('update_history')
        with open('sales_history.json', 'w') as json_file:
            json.dump(sales_history, json_file)
    
    elif confirm == 'n' or confirm_overwrite == 'n':
        return
    else:
        update()
    
    print_output.print_alert('stock_data')

def updateinv():
    confirm = input('Are you sure you want to update? This means overwriting your current stock and history data. (y/n) ')
    if confirm == 'y':
        errors = validate_data('inventory')
        if errors:
            print('Please resolve errors before updating stock')
            return
        inventory = inv_worksheet.get_all_values()[1:]
        update_stock(inventory_list=inventory)
    elif confirm == 'n':
        return
    else:
        updateinv()
    
    print_output.print_alert('stock_data')

def priceof(gtin):
    if not gtin_exists(gtin):
        print_output.print_error('gtin_not_exist')
        return
    product = Product(gtin)
    print(product.get('price'))

def instock(gtin):
    if not gtin_exists(gtin):
        print_output.print_error('gtin_not_exist')
        return
    product = Product(gtin)
    print(product.get('qty'))

def dataof(gtin):
    product = Product(gtin)
    print_output.print_dataof(product)

def scrap():
    to_scrap = []
    print('Add items to todays scrap list\n')
    while True:
        gtin = input('Enter product gtin to scrap: ')

        if gtin_exists(gtin):
            qty = input('Enter quantity: ')
            try: int(qty)
            except ValueError:
                print('Invalid input: Quantity must be numeric')
                continue
            to_scrap.append([gtin, qty])
            if input('Add another product?(y/n) ') == 'y': continue
            else: break
        else:
            try:
                int(gtin)
                print_output.print_error('gtin_not_exist')
            except ValueError:
                print('Invalid input: GTIN must be numeric')
                continue
    
    for row in to_scrap:
        scrap_worksheet.append_row(row)


def help(command):
    print_output.print_help(command)

def execute_cmd(command):
    entire_command = command
    
    command_list = ['update', 'updateinv', 'priceof', 'instock', 'dataof', 'scrap', 'help', 'exit', '1', '2', '3', '4', '5', '6', '7', '8']
    takes_arg = ['priceof', 'instock', 'dataof', 'help']

    command = command.split(" ")

    if len(command[0]) < 1:
        return
    elif len(command) == 1:
        command = command[0]
        if command in takes_arg:
            print(f'Invalid usage of ({command}): {command} requires additional parameter')
            print(f'Please type "help {command}" to see correct usage.\n')
            return
    elif len(command) == 2:
        if command[0] == 'help' or command[0] == '7':
            if len(command[1]) > 1 and str(command[1]) in command_list:
                help(command[1])
                return
            else:
                print(f'Invalid usage of ({command[0]}): No such command: {command[1]}')
                print(f'Please type "help {command[0]}" to see correct usage.\n')
                return
        try:
            gtin = str(int(command[1]))
            command = command[0]
        except ValueError:
            command = command[0]
            print(f'Invalid usage of ({command}): GTIN must be numeric')
            return
    else:
        gtin = command[1]
        command = command[0]
        if command in command_list:
            print(f'Invalid usage of ({command}): {command} takes only 1 parameter')
            print(f'Please type "help {command}" to see correct usage.\n')
        else:
            print(f'No such command: {command}')
            return
    

    if 'update' == command or '1' == command:
        update()
    elif 'updateinv' == command or '2' == command:
        updateinv()
    elif 'priceof' == command or '3' == command[0]:
        command = 'priceof'
        priceof(gtin)
    elif 'instock' == command or '4' == command[0]:
        command = 'instock'
        instock(gtin)
    elif 'dataof' == command or '5' == command[0]:
        command = 'dataof'
        dataof(gtin)
    elif 'scrap' == command or '6' == command[0]:
        scrap()
    elif 'exit' == command or '8' == command[0]:
        exit()
    else:
        print(f'No such command: "{command}"')
        