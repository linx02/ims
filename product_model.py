from datetime import datetime, timedelta
import setup

stock_data = setup.stock_data
sales_history = setup.sales_history

class Product:
    """
    Class representing a product in stock.

    Args:
        gtin (str): The (fictional)Global Trade Item Number (GTIN) of the product.

    Attributes:
        name (str): Name of the product.
        price (str): Price of the product
        supplier_price (str): The supplier price / buying price of the product
        supplier (str): The name of the product's supplier.
        qty (str): The quantity of the product in stock.
        gtin (str): The (fictional)Global Trade Item Number (GTIN) of the product.

    Methods:
        get(info):
            Get specific information about the product.

        sold_scrap_items(time_period=None):
            Get the total quantity of the product sold and scrapped within a specified time period.

        compare_sales(time_period):
            Compare the sales of the product between the current date and a past date.

    """
    global stock_data
    global sales_history
    def __init__(self, gtin):
        for product in stock_data:
            if gtin == product[-1]:
                self.name = product[0]
                self.price = product[1]
                self.supplier_price = product[2]
                self.supplier = product[3]
                self.qty = product[4]
                self.gtin = gtin
    
    def get(self, info):
        """
        Get specific information about the product.

        Args:
            info (str): The information to retrieve. Supported values: 'price', 'supplier_price', 'supplier', 'qty', 'gtin'.

        Returns:
            str: String representing the product information in format 'product_name: value'.
        """
        # Format string
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
    
    def sold_scrap_items(self, time_period=None):
        """
        Get the total quantity of the product sold and scrapped within a specified time period.

        Args:
            time_period (int or tuple, optional): The time period to consider. If 'int', represents number of days from the current date. If 'tuple', represents a range of dates.

        Returns:
            tuple: Tuple containing two integers: (total_sold, total_scrap).
                   - total_sold (int): Total quantity of the product sold within the time period.
                   - total_scrap (int): Total quantity of the product scrapped within the time period.
        """
        # Generate date list
        if type(time_period) == int:
            current_date = datetime.now().date()
            date_list = [current_date - timedelta(days=i) for i in range(time_period)]

        else:
            start_datetime = time_period[0]
            end_datetime = time_period[1]

            date_list = [start_datetime + timedelta(days=i) for i in range((end_datetime - start_datetime).days + 1)]

        sold_items = []
        scrap_items = []

        # Iterate through data and append to lists
        for date in date_list:
            for item in sales_history:
                if item["date"] == str(date):
                    for sold in item["sold"]:
                        if sold[0] == self.gtin:
                            sold_items.append(sold)
                        
                    for scrap in item["scrap"]:
                        if scrap[0] == self.gtin:
                            scrap_items.append(scrap)
        
        # Calculate totals
        total_sold = 0
        for item in sold_items:
            total_sold += item[1]
        
        total_scrap = 0
        for item in scrap_items:
            total_scrap += item[1]
        
        return (total_sold, total_scrap)
    
    def compare_sales(self, time_period):
        """
        Compare the sales of the product between the same time period this and last year.

        Args:
            time_period (int): The number of days to consider.

        Returns:
            int: Difference in sales quantity between current time period and last year time period.
        """
        current_date = datetime.now().date()
        delta = timedelta(days=time_period)
        last_datetime = datetime(current_date.year - 1, current_date.month, current_date.day)
        last_datetime_start = last_datetime - delta
        last_date = last_datetime.date()
        last_date_start = last_datetime_start.date()

        last_sales = self.sold_scrap_items(time_period=[last_date_start, last_date])[0]
        current_sales = self.sold_scrap_items(time_period)[0]

        return current_sales - last_sales