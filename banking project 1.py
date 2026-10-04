import json
import random
import os
from datetime import datetime

FILE_NAME = "accounts.json"


# Load account data
def load_accounts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}


# Save account data
def save_accounts():
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)


accounts = load_accounts()


# Generate account number
def generate_account_number():
    while True:
        acc_no = str(random.randint(1000000000, 9999999999))
        if acc_no not in accounts:
            return acc_no


# Create account
def create_account():
    print("\n===== CREATE BANK ACCOUNT =====")

    name = input("Enter your name: ")
    phone = input("Enter phone number: ")

    if not name.strip() or not phone.strip():
        print("Name and phone number cannot be empty.")
        return

    pin = input("Create 4-digit PIN: ")

    if not pin.isdigit() or len(pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    acc_no = generate_account_number()

    accounts[acc_no] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "history": []
    }

    save_accounts()

    print("\nAccount created successfully!")
    print("Account Holder:", name)
    print("Account Number:", acc_no)
    print("Initial Balance: ₹0.00")
    print("Please remember your account number and PIN.")


# Record transaction
def record_transaction(acc_no, message):
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    accounts[acc_no]["history"].append(
        time + " - " + message
    )


# Check balance
def check_balance(acc_no):
    print("\n===== ACCOUNT BALANCE =====")
    print("Account Holder:", accounts[acc_no]["name"])
    print("Available Balance: ₹", accounts[acc_no]["balance"])


# Deposit money
def deposit(acc_no):
    print("\n===== DEPOSIT MONEY =====")

    try:
        amount = float(input("Enter amount to deposit: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        accounts[acc_no]["balance"] += amount

        record_transaction(
            acc_no, f"Deposited ₹{amount:.2f}"
        )

        save_accounts()

        print("Deposit successful!")
        print("Updated Balance: ₹", accounts[acc_no]["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# Withdraw money
def withdraw(acc_no):
    print("\n===== WITHDRAW MONEY =====")

    try:
        amount = float(input("Enter withdrawal amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > accounts[acc_no]["balance"]:
            print("Insufficient balance!")
        else:
            accounts[acc_no]["balance"] -= amount

            record_transaction(
                acc_no, f"Withdrawn ₹{amount:.2f}"
            )

            save_accounts()

            print("Withdrawal successful!")
            print("Remaining Balance: ₹", accounts[acc_no]["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# Transfer money
def transfer(acc_no):
    print("\n===== MONEY TRANSFER =====")

    receiver = input("Enter receiver account number: ")

    if receiver not in accounts:
        print("Receiver account not found!")
        return

    if receiver == acc_no:
        print("Cannot transfer money to your own account.")
        return

    try:
        amount = float(input("Enter transfer amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
        elif amount > accounts[acc_no]["balance"]:
            print("Insufficient balance!")
        else:
            accounts[acc_no]["balance"] -= amount
            accounts[receiver]["balance"] += amount

            record_transaction(
                acc_no,
                f"Transferred ₹{amount:.2f} to {receiver}"
            )

            record_transaction(
                receiver,
                f"Received ₹{amount:.2f} from {acc_no}"
            )

            save_accounts()

            print("Transfer successful!")

    except ValueError:
        print("Please enter a valid amount.")


# Transaction history
def transaction_history(acc_no):
    print("\n===== TRANSACTION HISTORY =====")

    history = accounts[acc_no]["history"]

    if not history:
        print("No transactions available.")
    else:
        for transaction in history:
            print(transaction)


# Change PIN
def change_pin(acc_no):
    print("\n===== CHANGE PIN =====")

    old_pin = input("Enter old PIN: ")

    if old_pin != accounts[acc_no]["pin"]:
        print("Incorrect old PIN!")
        return

    new_pin = input("Enter new 4-digit PIN: ")

    if not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    confirm_pin = input("Confirm new PIN: ")

    if new_pin == confirm_pin:
        accounts[acc_no]["pin"] = new_pin
        save_accounts()
        print("PIN changed successfully!")
    else:
        print("PIN confirmation does not match.")


# Account menu
def account_menu(acc_no):
    while True:
        print("\n========== ACCOUNT MENU ==========")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance(acc_no)

        elif choice == "2":
            deposit(acc_no)

        elif choice == "3":
            withdraw(acc_no)

        elif choice == "4":
            transfer(acc_no)

        elif choice == "5":
            transaction_history(acc_no)

        elif choice == "6":
            change_pin(acc_no)

        elif choice == "7":
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice! Please try again.")


# Login
def login():
    print("\n===== BANK LOGIN =====")

    acc_no = input("Enter account number: ")
    pin = input("Enter PIN: ")

    if acc_no in accounts and accounts[acc_no]["pin"] == pin:
        print("\nWelcome,", accounts[acc_no]["name"])
        account_menu(acc_no)
    else:
        print("Invalid account number or PIN!")


# Main menu
def main():
    while True:
        print("\n================================")
        print("       BANKING SYSTEM")
        print("================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Thank you for using our Banking System!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()