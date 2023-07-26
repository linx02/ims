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