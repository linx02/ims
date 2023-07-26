from product_model import *
import print_output
import re
from setup import *

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
    print_output.print_dataof(product)

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