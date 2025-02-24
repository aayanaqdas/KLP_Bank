import json  # Lagring av data
import os  # Lese og skrive i JSON filen
import random  # Generering av random tall for kontonummer

# Fargekoder for terminalutskrift
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE_ITALIC = "\033[3;94m"
RESET = "\033[0m"  # Tilbakestill farge

# Filnavn for lagring av bankdata
DATA_FILE = "data.json"

# Lagrer brukernavnet globalt for å hente inn bruker data
current_user = None

# Funksjon for å laste inn bankdata fra JSON-fil
def load_bank_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file: # Lager JSON filen om den ikke eksisterer
            json.dump({"users": {}}, file, indent=4) # Setter inn users objektet
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

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
    print(f"{YELLOW}Velkommen {current_user['name']} {RESET}")
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
        display_balance("all", 0, "display")
    elif choice == "2":
        account_type = select_account_type()
        deposit(account_type)
    elif choice == "3":
        account_type = select_account_type()
        withdraw(account_type)
    elif choice == "4":
        global current_user
        current_user = None  # Reset bruker
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
    username = input("Tast inn ditt brukernavn for å logge inn eller tast 1 for å gå tilbake: ")

    if username == "1":
        print_start_menu()
    elif username in bank_users:
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
        new_user = {
            "username": username,
            "name": name,
            "accounts": {
                "brukskonto": {
                    "account_number": generate_account_num(bank_users),
                    "balance": 0
                },
                "sparekonto": {
                    "account_number": generate_account_num(bank_users),
                    "balance": 0
                }
            }
        }

        bank_users[username] = new_user
        save_data(bank_data)
        current_user = bank_users[username]

        print(f"{GREEN}\nBruker opprettet med brukernavn: {username}{RESET}")

        print_main_menu()

# Funksjon for å generere et unikt 11 sifret kontonummer
# Går gjennom alle kontonummer på hver bruker for å ikke generere den samme
def generate_account_num(existing_users):
    existing_account_numbers = set()
    for user in existing_users.values():
        for account in user["accounts"].values():
            existing_account_numbers.add(account["account_number"])

    while True:
        account_number = str(random.randint(10000000000, 99999999999))
        if account_number not in existing_account_numbers:
            return account_number

# Funksjon for å sjekke saldo
def display_balance(account_type, amount, action):
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    user_accounts = bank_users[current_user["username"]]["accounts"]

    print(BLUE_ITALIC + "\n-------------------- Saldo --------------------" + RESET)
    if action == "deposit":
        # Viser saldo kun til den kontoen du satte inn penger
        print(f"{GREEN}+{amount}{RESET}")
        print(f"{YELLOW}{account_type}: {user_accounts[account_type]['balance']} kr{RESET}")
    elif action == "withdraw":
        # Viser saldo kun til den kontoen du tok ut penger fra
        print(f"{RED}-{amount}{RESET}")
        print(f"{YELLOW}{account_type}: {user_accounts[account_type]['balance']} kr{RESET}")
    else:
        # Viser saldo på alle kontoene
        for account_type, account_info in user_accounts.items():
            print(f"{YELLOW}{account_type}: {account_info['balance']} kr{RESET}")

    input("Trykk enter for å gå tilbake ")
    print_main_menu()

# Funksjon for å sette inn penger
def deposit(account_type):
    handle_transaction(account_type, "deposit")

# Funksjon for å ta ut penger
def withdraw(account_type):
    handle_transaction(account_type, "withdraw")

# Funksjon for å håndtere transaksjoner (ta ut/sette inn)
def handle_transaction(account_type, transaction_type):
    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_balance = bank_users[current_user["username"]]["accounts"][account_type]["balance"]

    print(f"{BLUE_ITALIC}\n-------------------- {"Sett inn" if transaction_type == "deposit" else "Ta ut"} --------------------{RESET}")
    print(f"{YELLOW}{current_user['name']}")
    print(f"Saldo: {current_balance} kr")
    print(f"Kontonummer: {current_user['accounts'][account_type]['account_number']}{RESET}")
    print("\n1. Sett inn penger" if transaction_type == "deposit" else "\n1. Ta ut penger")
    print("2. Gå tilbake")
    print(f"{BLUE_ITALIC}-------------------------------------------------{RESET}")

    choice = input("Tast inn ditt valg:  ")

    if choice == "1":
        amount = int(input(f"\nBeløp du vil {'sette inn' if transaction_type == 'deposit' else 'ta ut'}: "))

        if transaction_type == "deposit":
            if amount <= 0:
                input(RED + "Ugyldig beløp! Trykk enter for å prøve igjen " + RESET)
                handle_transaction(account_type, transaction_type)
            else:
                new_balance = current_balance + amount
        else:
            if amount > current_balance:
                input(RED + "Du har ikke nok penger på konto! Trykk enter for å prøve igjen " + RESET)
                handle_transaction(account_type, transaction_type)
            else:
                new_balance = current_balance - amount

        bank_users[current_user["username"]]["accounts"][account_type]["balance"] = new_balance
        save_data(bank_data)

        display_balance(account_type, amount, transaction_type)
    elif choice == "2":
        print_main_menu()
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen. Trykk Enter for å prøve igjen{RESET}")
        handle_transaction(account_type, transaction_type)

# Funksjon for å velge kontotype
def select_account_type():
    print(f"\n{BLUE_ITALIC}------------------ Velg Konto ------------------{RESET}")
    print(" 1. Brukskonto")
    print(" 2. Sparekonto")
    print(f"{BLUE_ITALIC}---------------------------------------------------{RESET}")

    choice = input("Skriv inn tall for å velge konto: ")

    if choice == "1":
        return "brukskonto"
    elif choice == "2":
        return "sparekonto"
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-2). Trykk Enter for å prøve igjen{RESET}")
        return select_account_type()

# Start programmet
print_start_menu()