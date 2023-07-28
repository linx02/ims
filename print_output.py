sheet_link = 'https://docs.google.com/spreadsheets/d/18bCl8msVtXFvZ-By8N3ii_aQ5sm7WmIU6qxiguk63yA/edit?usp=sharing'

def print_main():
    """
    Print the main menu.

    Returns:
        None: The function prints the main menu to the console.
    """
    print(
f"""
*-------------------*
|     YourStore     |
|        IMS        |
*-------------------*
| Commands:         |
|                   |
| 1. update         |
| 2. updateinv      |
| 3. priceof [GTIN] |
| 4. instock [GTIN] |
| 5. dataof [GTIN]  |
| 6. scrap          |
| 7. help [COMMAND] |
| 8. exit           |
*-------------------*
Use either assigned numbers or command names e.g:
3 [GTIN] or priceof [GTIN]

Link to worksheets: {sheet_link}
"""
)

def print_dataof(product):
    """
    Print info and statistics about a product.

    Args:
        product (Product): Product object containing info about the product.

    Returns:
        None: The function prints product info.
    """
    
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
    Sold(7 days): {product.sold_scrap_items(7)[0]}
    -------------
    Sold(30 days): {product.sold_scrap_items(30)[0]}
    --------------
    Change in sales (7 days): {product.compare_sales(7)}
    -------------------------
    Change in sales (30 days): {product.compare_sales(30)}
    --------------------------
    Scrap(7 days): {product.sold_scrap_items(7)[1]}
    --------------
    Scrap(30 days): {product.sold_scrap_items(30)[1]}
    ---------------
    """
        )
    
def print_loading(index):
    """
    Print loading messages based on the provided index.

    Args:
        index (str): The index of the loading task.

    Returns:
        None: The function prints the loading message.
    """
    
    match index:
        case 'load_api':
            print('Connecting to google api...')
        case 'load_stock':
            print('Loading stock data...')
        case 'load_history':
            print('Loading history data...')
        case 'update_stock':
            print('Updating stock data...')
        case 'update_history':
            print('Updating history data...')
        case 'update_sheet':
            print('Updating sheet...')

def print_help(command):
    """
    Print help information for different commands.

    Args:
        command (str): The command for which help info is requested.

    Returns:
        None: The function prints help info.
    """
    
    match command:

        case 'update':
            purpose = 'Update the stores inventory data'
            description = 'Takes all data from sales and scraps sheets, subtracts the data from the stock sheet and adds the data to the sales history'
            usage = ['update', '1']
        case 'updateinv':
            purpose = 'Update the stores stock quantities from inventory list'
            description = 'Takes all data from inventory sheet and overwrites the appropriate quantities in the stock sheet'
            usage = ['updateinv', '2']
        case 'priceof':
            purpose = 'Search prices of products in inventory'
            description = 'Gets the price of given product identifier(GTIN number) from stock sheet and prints it to the screen'
            usage = ['priceof [GTIN]', '3 [GTIN]']
        case 'instock':
            purpose = 'Check quantity of products in inventory'
            description = 'Gets the quantity of given product identifier(GTIN number) from stock sheet and prints it to the screen'
            usage = ['instock [GTIN]', '4 [GTIN]']
        case 'dataof':
            purpose = 'Provide useful statistics and overviews of products in inventory'
            description = 'Gets all data of given product identifier(GTIN number) from stock sheet and prints it to the screen. Calculates increase/decrease in sales and scraps based on sales history data and prints it to the screen'
            usage = ['dataof [GTIN]', '5 [GTIN]']
        case 'scrap':
            purpose = 'Allow for scrapping of products straight from the system'
            description = 'Initiates an infinite loop where user can enter product identifiers(GTIN numbers) and quantity to scrap. Adds the data to the scrap sheet'
            usage = ['scrap', '6']
        case 'help':
            purpose = 'Provide instructions and context to commands in this system'
            description = 'Takes given command and prints appropriate purpose, description and usage of the command to the screen.'
            usage = ['help [COMMAND]', '7 [COMMAND]']
        case 'exit':
            purpose = 'Provide a way to exit/shutdown the system'
            description = 'Kills the script'
            usage = ['exit', '8']
    
    print(f'Command: {command}')
    print(f'Purpose: {purpose}')
    print(f'Description: {description}')
    print(f'Usage: "{usage[0]}" or "{usage[1]}"')

def print_alert(alert):
    """
    Print alert message based on provided alert type.

    Args:
        alert (str): The type of alert to display.

    Returns:
        None: The function prints an alert message.
    """
    match alert:

        case 'stock_data':
            alert = 'Restart needed for stock data to be reloaded in system'

    print(f'ALERT: {alert}')

def print_error(error, row=None):
    """
    Print error message based on the provided error type.

    Args:
        error (str): The type of error to be displayed.
        row (int, optional): Row number associated with the error.

    Returns:
        None: The function prints an error message.
    """
    match error:

        case 'invalid_data':
            error = f'Invalid data on row: {row}'
        
        case 'gtin_not_exist':
            error = f'no match for provided GTIN'
    
    print(f'ERROR: {error}')
