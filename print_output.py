def print_main():
    print(
"""
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
*-------------------*
Use either assigned numbers or command names e.g:
3 [GTIN] or priceof [GTIN]
"""
)

def print_dataof(product):
    
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
    + / - (7 days): {product.compare_sales(7)}
    ---------------
    + / - (30 days): {product.compare_sales(30)}
    ----------------
    Scrap(7 days): {product.sold_scrap_items(7)[1]}
    --------------
    Scrap(30 days): {product.sold_scrap_items(30)[1]}
    ---------------
    """
        )
    
def print_loading(index):
    
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
        case 'reload_data':
            print('Reloading data...')

def print_help(command):
    pass