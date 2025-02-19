import json
import os
import random

BANK_DATA = "data.json"

def load_bank_data():
    if os.path.exists(BANK_DATA):
        with open(BANK_DATA, "r") as file:
            return json.load(file)
    return {}


def print_start_menu():
    print("------------------ KLP Bank ------------------")
    print("| 1. Logg inn                                |")
    print("| 2. Opprett ny bruker                       |")
    print("----------------------------------------------")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_start_menu_choice(menu_choice)

def print_main_menu():
    print("------------------ KLP Bank ------------------")
    print("| 1. Se saldo                                |")
    print("| 2. Sett inn penger                         |")
    print("| 3. Ta ut penger                            |")
    print("| 4. Logg ut                                 |")
    print("----------------------------------------------")

def execute_start_menu_choice(choice):
    if choice == "1":
        login()
    elif choice == "2":
        create_user()
    else:
        print("Ugyldig valg! Vennligst velg et tall fra menyen")
        print_start_menu()

def create_user():
    bank_data = load_bank_data()
    bank_users = bank_data["users"]


    name = input("Skriv inn fornavn og etternavnet ditt: ")
    username = input("Skriv inn brukernavn: ").lower()

    if any(user["username"] == username for user in bank_users):
        print("Brukernavn er tatt! Vennligst velg en annen")
        create_user()
    else:
        account_number = generate_account_num(bank_users)
        new_user_data = {
            "username": username,
            "name": name,
            "account_number": account_number,
            "balance": 0  # Initial balance set to 0
        }
        bank_users.append(new_user_data)
        save_data(bank_data)
        print(f"Bruker opprettet med kontonummer: {account_number}")



def generate_account_num(existing_users):
    existing_account_numbers = {user["account_number"] for user in existing_users}
    
    while True:
        account_number = str(random.randint(10000000000, 99999999999))  # 11-digit number
        if account_number not in existing_account_numbers:
            return account_number

def login():
    username = input("Tast inn ditt brukernavn: ")

    

def save_data(data):
    with open(BANK_DATA, "w") as file:
        json.dump(data, file, indent=4)

print_start_menu()

    # if username in bank_users:
    #     print("Brukernavn eksisterer allerede. Vennligst oppgi nytt brukernavn")
    #     create_user()
    # else:
    #     account_number = generate_account_num()
    #     print(account_number)

    #     print(bank_users)
    #     new_user_data = {
    #         "name": name,
    #         "account_number": account_number,
    #         "balance": 0  # Initial balance set to 0
    #     }
    #     bank_users[username] = new_user_data
    #     bank_users["users"] = bank_users
    #     save_data(bank_data[username])