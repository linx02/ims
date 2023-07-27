import print_output
import functions

# Main loop of the program
def main():
    print_output.print_main()
    while True:
        command = input('YourStore > ')
        functions.execute_cmd(command)

main()