import json # Lagring av data
import os # Lese og skrive i JSON filen
import random # Generering av random tall for kontonummer

# Fargekoder for terminalutskrift
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE_ITALIC = "\033[3;94m"
RESET = "\033[0m"  # Tilbakestill farge

# Filnavn for lagring av bankdata
DATA_FILE = "data.json"

#Lagrer brukernavnet globalt for å hente inn bruker data
current_user = None 

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
    print(f"\n{BLUE_ITALIC}------------------ KLP Bank ------------------")
    print("| 1. Logg inn                                |")
    print("| 2. Opprett ny bruker                       |")
    print(f"----------------------------------------------{RESET}")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_start_menu_choice(menu_choice)

# Funksjon for å håndtere valg i startmenyen
def execute_start_menu_choice(choice):
    if choice == "1":
        login()
    elif choice == "2":
        create_user()
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-2). Trykk Enter for å prøve igjen{RESET}")
        print_start_menu()

# Funksjon for å vise hovedmenyen
def print_main_menu():
    print(f"\n{BLUE_ITALIC}------------------ KLP Bank ------------------{RESET}")
    print(f"{YELLOW}Velkommen {current_user["name"]} {RESET}")
    print("\n 1. Se saldo                                ")
    print(" 2. Sett inn penger                         ")
    print(" 3. Ta ut penger                            ")
    print(" 4. Logg ut                                 ")
    print(f"{BLUE_ITALIC}----------------------------------------------{RESET}")

    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_main_menu_choice(menu_choice)

# Funksjon for å håndtere valg i hovedmenyen
def execute_main_menu_choice(choice):
    if choice == "1":
        display_balance(0, "display")
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        global current_user
        current_user = None # Reset bruker
        print(f"{YELLOW}Logged out!{RESET}")
        print_start_menu()
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-4). Trykk Enter for å prøve igjen{RESET}")
        print_main_menu()

# Funksjon for å logge inn en bruker
def login():
    global current_user
    bank_data = load_bank_data()  # Henter inn all dataen i JSON-filen
    bank_users = bank_data["users"]  # Henter inn alle brukerne i JSON-filen

    print(f"{BLUE_ITALIC}\n-------------------- Login --------------------{RESET}")
    username = input("Tast inn ditt brukernavn for å logge inn: ")

    if username in bank_users:
        current_user = bank_users[username]
        print_main_menu()
    else:
        print(f"{RED}Ugyldig brukernavn. Vennligst prøv igjen!{RESET}")
        login()

# Funksjon for å opprette en ny bruker
def create_user():
    global current_user
    bank_data = load_bank_data()
    bank_users = bank_data["users"]


    print(f"{BLUE_ITALIC}\n-------------------- Opprett Bruker --------------------{RESET}")
    name = input("Skriv inn fulle navn: ")
    username = input("Skriv inn brukernavn: ").lower()

    if username in bank_users:
        print(f"{RED}Brukernavnet {BLUE_ITALIC}'{username}'{RED} er allerede tatt. Vennligst velg en annen{RESET}")
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

        current_user = bank_users[username]
        print_main_menu()

# Funksjon for å generere et unikt kontonummer
def generate_account_num(existing_users):
    # Funksjonen passer på å ikke generere kontonummer som allerede eksisterer ved å loope gjennom alle brukernes kontonummer
    existing_account_numbers = {user["account_number"] for user in existing_users.values()}
    
    while True:
        account_number = str(random.randint(10000000000, 99999999999))  # 11 siffer nummer
        if account_number not in existing_account_numbers:
            return account_number

# Funksjon for å sjekke saldo
def display_balance(amount, action):
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    balance = bank_users[current_user["username"]]["balance"]

    print( BLUE_ITALIC + "\n-------------------- Saldo --------------------" + RESET)
    if action == "deposit":
        print(f"{GREEN}+{amount}{RESET}")
    elif action == "withdraw":
        print(f"{RED}-{amount}{RESET}")

    print(f"{YELLOW}Saldo: {balance} kr{RESET}")
    input("Trykk enter for å gå tilbake ")
    print_main_menu()


# Funksjon for å sette inn penger
def deposit():
    # Henter inn oppdatert bruker info
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_balance = bank_users[current_user["username"]]["balance"]

    print(f"{BLUE_ITALIC}\n-------------------- Sett inn --------------------{RESET}")
    print(f"{YELLOW}{current_user["name"]}")
    print(f"Saldo: {current_balance} kr")
    print(f"Kontonummer: {current_user['account_number']}{RESET}")
    print("\n1. Sett inn penger")
    print("2. Gå tilbake")
    print(f"{BLUE_ITALIC}-------------------------------------------------{RESET}")

    choice = input("Tast inn ditt valg:  ")

    if choice == "1":
        amount = int(input("\nBeløp du vil sette inn: "))

        if amount < 0:
            input(RED + "Ugyldig beløp! Trykk enter for å prøve igjen " + RESET)
            deposit()
        else:
            new_balance = bank_users[current_user["username"]]["balance"] + amount
            bank_users[current_user["username"]]["balance"] = new_balance
            save_data(bank_data)

            display_balance(amount, "deposit")
    elif choice == "2":
        print_main_menu()
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen. Trykk Enter for å prøve igjen{RESET}")
        deposit()

# Funksjon for å ta ut penger
def withdraw():
    # Henter inn oppdatert bruker info
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_balance = bank_users[current_user["username"]]["balance"]

    print(f"{BLUE_ITALIC}\n-------------------- Ta ut --------------------{RESET}")
    print(f"{YELLOW}{current_user['name']}")
    print(f"Saldo: {current_balance} kr")
    print(f"Kontonummer: {current_user['account_number']}{RESET}")
    print("\n1. Ta ut penger")
    print("2. Gå tilbake")
    print(f"{BLUE_ITALIC}-----------------------------------------------{RESET}")

    choice = input("Tast inn ditt valg:  ")

    if choice == "1":
        amount = int(input("\nBeløp du vil ta ut: "))

        if amount > current_balance:
            input(RED + "Ugyldig beløp! Du har ikke nok penger på kontoen. Trykk enter for å prøve igjen " + RESET)
            withdraw()
        else:
            new_balance = bank_users[current_user["username"]]["balance"] - amount
            bank_users[current_user["username"]]["balance"] = new_balance
            save_data(bank_data)

            display_balance(amount, "withdraw")
    elif choice == "2":
        print_main_menu()
    else:
        print(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen{RESET}")
        withdraw()


# Start programmet
print_start_menu()