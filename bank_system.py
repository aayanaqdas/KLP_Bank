import json
import os
import random

# Fargekoder for terminalutskrift
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"  # Tilbakestill farge

# Filnavn for lagring av bankdata
DATA_FILE = "data.json"

# Funksjon for å laste inn bankdata fra JSON-fil
def load_bank_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"users": {}}

# Funksjon for å lagre bankdata til JSON-fil
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Funksjon for å vise startmenyen
def print_start_menu():
    print("\n------------------ KLP Bank ------------------")
    print("| 1. Logg inn                                |")
    print("| 2. Opprett ny bruker                       |")
    print("----------------------------------------------")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_start_menu_choice(menu_choice)

# Funksjon for å håndtere valg i startmenyen
def execute_start_menu_choice(choice):
    if choice == "1":
        login()
    elif choice == "2":
        create_user()
    else:
        print(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen{RESET}")
        print_start_menu()

# Funksjon for å vise hovedmenyen
def print_main_menu(user_obj):
    print("\n------------------ KLP Bank ------------------")
    print(f"{BLUE} Velkommen {user_obj['name']} {RESET}")
    print("| 1. Se saldo                                |")
    print("| 2. Sett inn penger                         |")
    print("| 3. Ta ut penger                            |")
    print("| 4. Logg ut                                 |")
    print("----------------------------------------------")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_main_menu_choice(menu_choice, user_obj)

# Funksjon for å håndtere valg i hovedmenyen
def execute_main_menu_choice(choice, user_obj):
    if choice == "1":
        check_balance(user_obj)
    elif choice == "2":
        deposit(user_obj)
    elif choice == "3":
        withdraw(user_obj)
    elif choice == "4":
        print(f"{YELLOW}Logged out!{RESET}")
        print_start_menu()
    else:
        print(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen{RESET}")
        print_main_menu(user_obj)

# Funksjon for å logge inn en bruker
def login():
    bank_data = load_bank_data()  # Henter inn all dataen i JSON-filen
    bank_users = bank_data["users"]  # Henter inn alle brukerne i JSON-filen

    print(f"{BLUE}\n-------------------- Login --------------------{RESET}")
    username = input("Tast inn ditt brukernavn for å logge inn: ")

    if username in bank_users:
        print_main_menu(bank_users[username])  # Sender inn brukerobjektet til print_main_menu for å få tilgang til brukerens detaljer
    else:
        print(f"{RED}Ugyldig brukernavn. Vennligst prøv igjen!{RESET}")
        login()

# Funksjon for å opprette en ny bruker
def create_user():
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    print(f"{BLUE}\n-------------------- Opprett Bruker --------------------{RESET}")
    name = input("Skriv inn fulle navn: ")
    username = input("Skriv inn brukernavn: ").lower()

    if username in bank_users:
        print(f"{RED}Brukernavnet {BLUE}'{username}'{RED} er allerede tatt. Vennligst velg en annen{RESET}")
        create_user()
    else:
        account_number = generate_account_num(bank_users)
        new_user = {
            "username": username,
            "name": name,
            "account_number": account_number,
            "balance": 0
        }

        bank_users[username] = new_user
        save_data(bank_data)
        print(f"{GREEN}\nBruker opprettet med brukernavn: {username} og kontonummer: {account_number}{RESET}")

        print_main_menu(bank_users[username])  # Bruker objektet lagret

# Funksjon for å generere et unikt kontonummer
def generate_account_num(existing_users):
    # Funksjonen passer på å ikke generere kontonummer som allerede eksisterer ved å loope gjennom alle brukernes kontonummer
    existing_account_numbers = {user["account_number"] for user in existing_users.values()}
    
    while True:
        account_number = str(random.randint(10000000000, 99999999999))  # 11 siffer nummer
        if account_number not in existing_account_numbers:
            return account_number

# Funksjon for å sjekke saldo
def check_balance(user_obj):
    # user_obj er en gammel versjon av bruker infoen som blir satt når man logger inn
    # Må derfor hente inn data på nytt for oppdatert info
    current_user = user_obj["username"]

    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    balance = bank_users[current_user]["balance"]

    print( BLUE + "\n-------------------- Saldo --------------------" + RESET)
    print(f"{GREEN}Saldo: {balance} kr{RESET}")
    input("Trykk enter for å gå tilbake ")
    print_main_menu(user_obj)

# Funksjon for å sette inn penger
def deposit(user_obj):
    # Henter inn oppdatert bruker info
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_user = user_obj["username"]
    current_balance = bank_users[current_user]["balance"]

    print(f"{BLUE}\n-------------------- Sett inn --------------------{RESET}")
    print(f"{YELLOW}{user_obj['name']}")
    print(f"Saldo: {current_balance} kr")
    print(f"Kontonummer: {user_obj['account_number']}{RESET}")

    amount = int(input("\nBeløp du vil sette inn: "))

    new_balance = bank_users[current_user]["balance"] + amount
    bank_users[current_user]["balance"] = new_balance
    save_data(bank_data)
    check_balance(user_obj)

# Funksjon for å ta ut penger
def withdraw(user_obj):
    # Henter inn oppdatert bruker info
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_user = user_obj["username"]
    current_balance = bank_users[current_user]["balance"]

    print(f"{BLUE}\n-------------------- Ta ut --------------------{RESET}")
    print(f"{YELLOW}{user_obj['name']}")
    print(f"Saldo: {current_balance} kr")
    print(f"Kontonummer: {user_obj['account_number']}{RESET}")

    amount = int(input("\nBeløp du vil ta ut: "))

    if amount > current_balance:
        print(f"{RED}Ugyldig beløp! Du har ikke nok penger på kontoen.{RESET}")
        withdraw(user_obj)
    else:
        new_balance = bank_users[current_user]["balance"] - amount
        bank_users[current_user]["balance"] = new_balance
        save_data(bank_data)
        check_balance(user_obj)

# Start programmet
print_start_menu()