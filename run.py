import print_output
import functions

def main():
    """
    Main function of the program.

    Returns:
        None: The function does not return any value. Runs until user exits the program.
    """
    print_output.print_main()
    while True:
        command = input('YourStore > ')
        functions.execute_cmd(command)

main()