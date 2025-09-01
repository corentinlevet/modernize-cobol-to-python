"""Converted from `main.cob` — interactive menu runner.
"""
from operations import perform_operation


def main():
    continue_flag = True
    while continue_flag:
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            perform_operation('TOTAL')
        elif choice == '2':
            perform_operation('CREDIT')
        elif choice == '3':
            perform_operation('DEBIT')
        elif choice == '4':
            continue_flag = False
        else:
            print("Invalid choice, please select 1-4.")

    print("Exiting the program. Goodbye!")


if __name__ == '__main__':
    main()
