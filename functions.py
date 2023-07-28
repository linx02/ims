from product_model import *
import print_output
from setup import *

def gtin_exists(gtin):
    """
    Check if a GTIN (Global Trade Item Number) exists in the stock data.

    Args:
        gtin (str or int): The GTIN to check for existence in the stock data.

    Returns:
        bool: True if the GTIN exists in the stock data, False otherwise.
    """
    global stock_data
    for row in stock_data:
        if str(gtin) == row[-1]: return True

def validate_data(*args):
    """
    Validate data from one or more worksheets.

    Args:
        *args (str): Worksheet names to validate. Use 'sales', 'scraps', or 'inventory' to specify the worksheets.

    Returns:
        bool: True if there are any validation errors, False otherwise.
    """

    errors = False
    def validate(worksheet):
        nonlocal errors
        for row_index, item in enumerate(worksheet): # Loop through worksheet
            if len(item) > 3: # Check only GTIN and qty columns are filled
                print_output.print_error('invalid_data', row=row_index + 1)
                errors = True
                continue
            if not gtin_exists(item[0]): # Check gtin exists
                print_output.print_error('invalid_data', row=row_index + 1)
                errors = True
                continue
            try: # Check cell data are of type int
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
    """
    Update stock quantities based on sales, scraps, and inventory lists.

    Args:
        sales (list of lists, optional): A list of lists representing the sales data, list items should contain GTIN and quantity sold.
        scraps (list of lists, optional): A list of lists representing the scraps data, list items should contain GTIN and quantity of scraps.
        inventory_list (list of lists, optional): A list of lists representing the inventory data, list items should contain GTIN and the quantity to update in stock.

    Returns:
        bool: True if there are any errors during the update, False otherwise.
    """
    print_output.print_loading('update_stock')

    cols = 'ABCDEF' # Define column indexes for use with sheet.update()

    def update_qty(list_to_use):
        """
        Update stock quantities based on the provided list.

        Args:
            list_to_use (list of lists): A list of lists representing sales or scraps data, list items should contain GTIN and quantity.

        Returns:
            bool: True if there are any errors during the update, False otherwise.
        """
        for product in list_to_use:
            cell = stock_worksheet.find(product[0]) # Find cell of product with correct gtin
            qty_cell = stock_worksheet.cell(cell.row, cell.col - 1) # Cell of qty for same gtin

            index = cols[cell.col - 2] # Define column index to use
            try:
                stock_worksheet.update(f'{index}{cell.row}', int(qty_cell.value) - int(product[1])) # Subtract sales and update the sheet
            except Exception as e:
                print_output.print_error('invalid_data', cell.row)
                print('Please resolve errors before updating')
                return True
    
    if sales != None:
        errors = update_qty(sales)
        if errors: return True
    if scraps != None:
        errors = update_qty(scraps)
        if errors: return True

    if inventory_list != None:
        for product in inventory_list:
            cell = stock_worksheet.find(product[0])

            index = cols[cell.col - 2]
            stock_worksheet.update(f'{index}{cell.row}', int(product[1])) # Update sheet without subtraction for updateinv


def update():
    """
    Update stock data and sales history.

    Returns:
        None: The function does not return any value.
    """
    confirm_overwrite = 'n'
    confirm = input('Are you sure you want to update?\nThis means overwriting your current stock and history data. (y/n) ')

    if confirm != 'y': return

    if sales_history[-1]["date"] == str(datetime.now().date()): # Check if date already in history data
        confirm_overwrite = input('Todays date already exists in the sales history.\nAre you sure you want to overwrite it? (y/n) ')
        if confirm_overwrite != 'y': return

    if confirm == 'y':

        errors = validate_data('sales', 'scraps')

        if errors: # Abort if data invalid
            print('Please resolve errors before updating data')
            return

        sales = sales_worksheet.get_all_values()[1:]
        scraps = scrap_worksheet.get_all_values()[1:]

        errors = update_stock(sales=sales, scraps=scraps) # Update stock
        if errors: return

        # Make all values integers
        for item in sales:
            item[1] = int(item[1])
        
        for item in scraps:
            item[1] = int(item[1])

        # Define data structure to be appended
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

        # Save data in history
        with open('sales_history.json', 'w') as json_file:
            json.dump(sales_history, json_file)
    
    
    print_output.print_alert('stock_data')

def updateinv():
    """
    Update stock data with inventory information.

    Returns:
        None: The function does not return any value.
    """
    confirm = input('Are you sure you want to update? This means overwriting your current stock data. (y/n) ')
    if confirm == 'y':
        errors = validate_data('inventory')
        if errors: # Abort if invalid data
            print('Please resolve errors before updating stock')
            return
        inventory = inv_worksheet.get_all_values()[1:]
        update_stock(inventory_list=inventory) # Update stock
    else:
        return
    
    print_output.print_alert('stock_data')

def priceof(gtin):
    """
    Get the price of a product with the given GTIN.

    Args:
        gtin (str or int): The GTIN of the product to get price of.

    Returns:
        None: Prints price of product if the GTIN exists, otherwise returns None.
    """
    if not gtin_exists(gtin):
        print_output.print_error('gtin_not_exist')
        return
    product = Product(gtin)
    print(product.get('price'))

def instock(gtin):
    """
    Check the stock quantity of a product with the given GTIN.

    Args:
        gtin (str or int): The GTIN of the product to check quantity of.

    Returns:
        None: Prints stock quantity of product if the GTIN exists, otherwise returns None.
    """
    if not gtin_exists(gtin):
        print_output.print_error('gtin_not_exist')
        return
    product = Product(gtin)
    print(product.get('qty'))

def dataof(gtin):
    """
    Print data and statistics of a product with the given GTIN.

    Args:
        gtin (str or int): The GTIN of the product to get data of.

    Returns:
        None: Prints data of the product if the GTIN exists, otherwise returns None.
    """
    if not gtin_exists(gtin):
        print_output.print_error('gtin_not_exist')
        return
    product = Product(gtin)
    print_output.print_dataof(product)

def scrap():
    """
    Add items to the scrap list for the current day.

    Returns:
        None: The function does not return any value.
    """
    to_scrap = []
    print('Add items to todays scrap list\n')
    while True: # Initiate loop
        gtin = input('Enter product gtin to scrap: ')

        if gtin_exists(gtin):
            qty = input('Enter quantity: ')
            try: int(qty) # Validate input
            except ValueError:
                print('Invalid input: Quantity must be numeric')
                break
            to_scrap.append([gtin, qty])
            if input('Add another product?(y/n) ') == 'y': continue
            else: break
        else:
            try:
                int(gtin)
                print_output.print_error('gtin_not_exist')
                break
            except ValueError:
                print('Invalid input: GTIN must be numeric')
                break
    
    for row in to_scrap:
        scrap_worksheet.append_row(row) # Add to scrap worksheet


def help(command):
    """
    Display help information for a specific command.

    Args:
        command (str): The command for which help information is to be displayed.

    Returns:
        None: The function does not return any value.
    """
    print_output.print_help(command)

def execute_cmd(command):
    """
    Execute a command based on user input.

    Args:
        command (str): The command entered by the user.

    Returns:
        None: The function does not return any value. It performs actions based on the provided command.
    """
    
    # Define allowed commands and those which require additional parameters
    command_list = ['update', 'updateinv', 'priceof', 'instock', 'dataof', 'scrap', 'help', 'exit', '1', '2', '3', '4', '5', '6', '7', '8']
    takes_arg = ['priceof', 'instock', 'dataof', 'help']

    command = command.split(" ") # Split input into list [command, gtin/command]

    # Clear list of whitespace
    cleared_command = []
    for item in command:
        if len(item.strip()) > 0:
            cleared_command.append(item)
    command = cleared_command

    # Validate input
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
            if len(command[1]) > 0 and str(command[1]) in command_list and command[1].isdigit() == False:
                help(command[1])
                return
            else:
                print(f'Invalid usage of ({command[0]}): No such command: {command[1]}')
                print(f'Please type "help {command[0]}" to see correct usage.\n')
                return
        elif len(command[1]) > 0 and command[0] not in takes_arg:
            print(f'Invalid usage of {command[0]}: {command[0]} takes only 1 parameter')
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
            return
        else:
            print(f'No such command: {command}')
            return
    
    # Execute appropriate command
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
        