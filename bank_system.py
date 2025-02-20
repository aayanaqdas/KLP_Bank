import json
import os
import random

RED = "\033[91m"     
GREEN = "\033[92m"   
YELLOW = "\033[93m"  
BLUE = "\033[94m"  
RESET = "\033[0m"    # Tilbakestill farge


DATA_FILE = "data.json"

def load_bank_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def print_start_menu():
    print("\n------------------ KLP Bank ------------------")
    print("| 1. Logg inn                                |")
    print("| 2. Opprett ny bruker                       |")
    print("----------------------------------------------")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_start_menu_choice(menu_choice)

def execute_start_menu_choice(choice):
    if choice == "1":
        login()
    elif choice == "2":
        create_user()
    else:
        print( RED + "Ugyldig valg! Vennligst velg et tall fra menyen" + RESET)
        print_start_menu()

def print_main_menu(user):
    print("\n------------------ KLP Bank ------------------")
    print( BLUE + f" Velkommen {user["name"]}     " + RESET)
    print("| 1. Se saldo                                |")
    print("| 2. Sett inn penger                         |")
    print("| 3. Ta ut penger                            |")
    print("| 4. Logg ut                                 |")
    print("----------------------------------------------")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_main_menu_choice(menu_choice, user)

def execute_main_menu_choice(choice, user):
    if choice == "1":
        print(f"Saldo: {user['balance']} kr")
        print_main_menu(user)
    elif choice == "2":
        # transfer()
        print("transfer")
    else:
        print( RED + "Ugyldig valg! Vennligst velg et tall fra menyen" + RESET)
        print_main_menu(user)
    

def login():
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    print( BLUE + "\n-------------------- Login --------------------" + RESET)
    username = input("Tast inn ditt brukernavn for å logge inn: ")

    if username in bank_users:
        print_main_menu(bank_users[username]) # Sender inn brukerobjektet til print_main_menu for å få tilgang til brukerens detaljer
    else:
        print( RED + "Ugyldig brukernavn. Vennligst prøv igjen!" + RESET)
        login()


def create_user():
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    print( BLUE + "\n-------------------- Opprett Bruker --------------------" + RESET)
    name = input("Skriv inn fulle navn: ")
    username = input("Skriv inn brukernavn: ").lower()

    if username in bank_users:
        print(RED + f"Brukernavnet '{YELLOW + username + RED}' er allerede tatt. Vennligst velg en annen" + RESET)
        create_user()
    else:
        account_number = generate_account_num(bank_users)
        new_user = {
            "name": name,
            "account_number": account_number,
            "balance": 0
        }

        bank_users[username] = new_user
        save_data(bank_data)
        print(GREEN + f"\nBruker opprettet med brukernavn: {username} og kontonummer: {account_number}" + RESET)

        print_main_menu(bank_users[username])

    


def generate_account_num(existing_users):
    # Funksjonen passer på å ikke generere kontonummer som allerede eksisterer ved å loope gjennom alle brukernes kontonummer
    existing_account_numbers = {user["account_number"] for user in existing_users.values()}
    
    while True:
        account_number = str(random.randint(10000000000, 99999999999))  # 11 siffer nummer
        if account_number not in existing_account_numbers:
            return account_number

    

print_start_menu()
