import print_output
import functions

def main():
    print_output.print_main()
    while True:
        command = input('YourStore > ')
        functions.execute_cmd(command)

main()