import json
import os
import random

# Fargekoder for terminalutskrift
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE_ITALIC = "\033[3;94m"
RESET = "\033[0m"  # Tilbakestill farge

# Filnavn for lagring av bankdata
DATA_FILE = "data.json"

# Global variabel for å lagre brukernavnet til den innloggede brukeren
current_user = None




# Funksjon for å laste inn bankdata fra JSON-fil
def load_bank_data():
    """
    Laster inn bankdata fra en JSON-fil.
    Returnerer:
        dict: Bankdata som et Python-objekt.
    """

    # Sjekker om datafilen eksisterer, hvis ikke opprettes den
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({"users": {}}, file, indent=4)  # Oppretter en tom "users" objekt
    # Leser inn data fra filen og returnerer den som et Python-objekt
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Funksjon for å lagre bankdata til JSON-fil
def save_data(data):
    """
    Lagrer bankdata til en JSON-fil.
    Parametere:
        data (dict): Bankdata som skal lagres.
    """

    # Skriver data til filen i JSON-format
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)




# Funksjon for å vise startmenyen
def print_start_menu():
    print(f"\n{BLUE_ITALIC}------------------ KLP Bank ------------------")
    print("| 1. Logg inn                                |")
    print("| 2. Opprett ny bruker                       |")
    print(f"----------------------------------------------{RESET}")

    # Tar imot brukerens valg og sender det til funksjonen som håndterer valget
    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_start_menu_choice(menu_choice)

# Funksjon for å håndtere valg i startmenyen
def execute_start_menu_choice(choice):
    """
    Håndterer brukerens valg i startmenyen.
    Parametere:
        choice (str): Brukerens valg.
    """

    if choice == "1":
        login()
    elif choice == "2":
        create_user()
    else:
        print(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-2).{RESET}")
        print_start_menu()




# Funksjon for å vise hovedmenyen
def print_main_menu():
    print(f"\n{BLUE_ITALIC}------------------ KLP Bank ------------------{RESET}")
    print(f"{YELLOW}Velkommen {current_user['name']} {RESET}")
    print("\n 1. Se saldo                                ")
    print(" 2. Sett inn penger                         ")
    print(" 3. Ta ut penger                            ")
    print(" 4. Overfør penger mellom kontoer           ")
    print(" 5. Logg ut                                 ")
    print(f"{BLUE_ITALIC}----------------------------------------------{RESET}")

    # Tar imot brukerens valg og sender det til funksjonen som håndterer valget
    menu_choice = input("Skriv inn tall for å velge fra menyen: ")
    execute_main_menu_choice(menu_choice)

# Oppdaterer funksjonen for å håndtere valg i hovedmenyen
def execute_main_menu_choice(choice):
    """
    Håndterer brukerens valg i hovedmenyen.
    Parametere:
        choice (str): Brukerens valg.
    """

    if choice == "1":
        display_balance()
    elif choice == "2":
        account_type = select_account_type()  # Velger kontotype
        deposit(account_type)  # Sender inn konto type brukskonto/sparekonto
    elif choice == "3":
        account_type = select_account_type()
        withdraw(account_type)  # Sender inn konto type brukskonto/sparekonto
    elif choice == "4":
        transfer()
    elif choice == "5":
        global current_user
        current_user = None  # Nullstiller brukeren
        print(f"{YELLOW}Logged out!{RESET}")
        print_start_menu()
    else:
        print(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-5).{RESET}")
        print_main_menu()



# Funksjon for å logge inn en bruker
def login():
    global current_user
    bank_data = load_bank_data()  # Laster inn bankdata fra fil
    bank_users = bank_data["users"]  # Henter ut brukerne fra dataen

    print(f"{BLUE_ITALIC}\n-------------------- Login --------------------{RESET}")
    username = input("Tast inn ditt brukernavn for å logge inn eller tast 1 for å gå tilbake: ")

    if username == "1":
        print_start_menu()
    elif username in bank_users:
        current_user = bank_users[username]  # Setter den innloggede brukeren til global variabel
        print_main_menu()
    else:
        print(f"{RED}Ugyldig brukernavn. Vennligst prøv igjen!{RESET}")
        login()





# Funksjon for å opprette en ny bruker
def create_user():
    global current_user
    bank_data = load_bank_data()  # Laster inn bankdata fra fil
    bank_users = bank_data["users"]  # Henter ut brukerne fra dataen

    print(f"{BLUE_ITALIC}\n-------------------- Opprett Bruker --------------------{RESET}")
    name = input("Skriv inn fulle navn eller trykk 1 for å gå tilbake: ")
    if name == "1": print_start_menu()

    username = input("Skriv inn brukernavn eller trykk 1 for å gå tilbake: ").lower()
    if username == "1": print_start_menu()

    
    if username in bank_users:
        # Gir beskjed om at brukernavnet er tatt og prøver på nytt
        print(f"{RED}Brukernavnet {BLUE_ITALIC}'{username}'{RED} er allerede tatt. Vennligst velg en annen{RESET}")
        create_user()
    else:
        # Oppretter en ny bruker med to kontoer
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

        bank_users[username] = new_user  # Legger til den nye brukeren i dataen
        save_data(bank_data)  # Lagrer dataen til fil
        current_user = bank_users[username]  # Setter den innloggede brukeren

        print(f"{GREEN}\nBruker opprettet med brukernavn: {username}{RESET}")

        print_main_menu()





# Funksjon for å generere et unikt 11-sifret kontonummer
def generate_account_num(existing_users):
    """
    Genererer et unikt 11-sifret kontonummer.
    Parametere:
        existing_users (dict): Eksisterende brukere for å unngå duplikater.
    Returnerer:
        str: Et unikt 11-sifret kontonummer.
    """
    existing_account_numbers = set()
    # Samler alle eksisterende kontonummer for å unngå duplikater
    for user in existing_users.values():
        for account in user["accounts"].values():
            existing_account_numbers.add(account["account_number"])

    while True:
        account_number = str(random.randint(10000000000, 99999999999))
        if account_number not in existing_account_numbers:
            return account_number
        



# Funksjon for å sjekke saldo
def display_balance(account_type="all", amount=0, action="display"):
    """
    Viser saldoen til brukeren.
    Parametere:
        account_type (str): Typen konto (brukskonto eller sparekonto).
        amount (int): Beløpet som ble satt inn eller tatt ut.
        action (str): Handlingen som ble utført (deposit, withdraw, display).
    """
    bank_data = load_bank_data()  # Laster inn bankdata fra fil
    bank_users = bank_data["users"]  # Henter ut brukerne fra dataen

    user_accounts = bank_users[current_user["username"]]["accounts"]  # Henter ut kontoene til den innloggede brukeren

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
    """
    Setter inn penger på en spesifisert konto.
    Parametere:
        account_type (str): Typen konto (brukskonto eller sparekonto).
    """

    handle_transaction(account_type, "deposit")

# Funksjon for å ta ut penger
def withdraw(account_type):
    """
    Tar ut penger fra en spesifisert konto.
    Parametere:
        account_type (str): Typen konto (brukskonto eller sparekonto).
    """

    handle_transaction(account_type, "withdraw")




# Funksjon for å håndtere transaksjoner (ta ut/sette inn)
def handle_transaction(account_type, transaction_type):
    """
    Håndterer transaksjoner som innskudd og uttak.
    Parametere:
        account_type (str): Typen konto (brukskonto eller sparekonto).
        transaction_type (str): Typen transaksjon (deposit eller withdraw).
    """


    bank_data = load_bank_data()
    bank_users = bank_data["users"]

    current_balance = bank_users[current_user["username"]]["accounts"][account_type]["balance"]  # Henter saldoen til kontoen

    print(f"{BLUE_ITALIC}\n-------------------- {'Sett inn' if transaction_type == 'deposit' else 'Ta ut'} --------------------{RESET}")
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
                # Gir beskjed om ugyldig beløp og prøver på nytt
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

        bank_users[current_user["username"]]["accounts"][account_type]["balance"] = new_balance  # Oppdaterer saldoen
        save_data(bank_data)

        display_balance(account_type, amount, transaction_type)
    elif choice == "2":
        print_main_menu()
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen. Trykk Enter for å prøve igjen{RESET}")
        handle_transaction(account_type, transaction_type)



def transfer():
    """
    Overfører penger mellom kontoer.
    """
    bank_data = load_bank_data() 
    bank_users = bank_data["users"] 

    user_accounts = bank_users[current_user["username"]]["accounts"]

    print(f"{BLUE_ITALIC}\n-------------------- Overfør Penger --------------------{RESET}")
    print(f"{YELLOW}{current_user['name']}{RESET}")
    for account_type, account_info in user_accounts.items():
        print(f"{YELLOW}{account_type}: {account_info['balance']} kr{RESET}")
    
    print("\n1. Overføre til andre")
    print("2. Overføre mellom egne kontoer")
    print("3. Gå tilbake")

    choice = input("\nVelg fra menyen: ")

    if choice == "1":
        # Overføre til andre
        recipient_account_number = input("Skriv inn mottakerens kontonummer: ")
        recipient_account = None
        recipient_name = None

        # Finn mottakerens konto
        for user, user_data in bank_users.items():
            for account_type, account_info in user_data["accounts"].items():
                if account_info["account_number"] == recipient_account_number:
                    recipient_account = account_info
                    recipient_name = user
                    break
            if recipient_account:
                break

        if not recipient_account:
            input(f"{RED}Ugyldig kontonummer! Trykk Enter for å prøve igjen.{RESET}")
            transfer()
            return

        from_account = select_account_type("transfer_from")
        from_balance = bank_users[current_user["username"]]["accounts"][from_account]["balance"]

        print(f"\n{YELLOW}Saldo på {from_account}: {from_balance} kr{RESET}")
        print(f"Overfører til '{BLUE_ITALIC + recipient_name + RESET}' med kontonummer {recipient_account_number}")
        amount = int(input(f"\nBeløp du vil overføre fra {from_account} til {recipient_account_number}: "))

        if amount <= 0 or amount > from_balance:
            input(f"{RED}Ugyldig beløp! Trykk Enter for å prøve igjen.{RESET}")
            transfer()
            return

        # Oppdaterer saldoene
        bank_users[current_user["username"]]["accounts"][from_account]["balance"] -= amount
        recipient_account["balance"] += amount

        save_data(bank_data)  # Lagrer dataen til fil

        print(f"{GREEN}Overføring vellykket!{RESET}")
        display_balance() 

    elif choice == "2":
        # Overføre mellom egne kontoer
        from_account = select_account_type("transfer_from")
        from_balance = bank_users[current_user["username"]]["accounts"][from_account]["balance"]

        to_account = select_account_type("transfer_to")

        if from_account == to_account:
            input(f"{RED}Du kan ikke overføre penger til samme konto. Trykk Enter for å prøve igjen.{RESET}")
            transfer()
            return

        print(f"\n{YELLOW}Saldo på {from_account}: {from_balance} kr{RESET}")
        amount = int(input(f"Beløp du vil overføre fra {from_account} til {to_account}: "))

        if amount <= 0 or amount > from_balance:
            input(f"{RED}Ugyldig beløp! Trykk Enter for å prøve igjen.{RESET}")
            transfer()
            return

        # Oppdaterer saldoene
        bank_users[current_user["username"]]["accounts"][from_account]["balance"] -= amount
        bank_users[current_user["username"]]["accounts"][to_account]["balance"] += amount

        save_data(bank_data)

        print(f"{GREEN}Overføring vellykket!{RESET}")
        display_balance()

    elif choice == "3":
        print_main_menu()
    else:
        input(f"{RED}Ugyldig valg! Trykk Enter for å prøve igjen.{RESET}")
        transfer()





# Funksjon for å velge kontotype
def select_account_type(action=None):
    """
    Viser en meny for å velge kontotype og returnerer brukerens valg.
    Parametere :
        action (str): type handling man skal gjøre. Betemmer hva som står på inputen
    Returnerer:
        str: Valgt kontotype (brukskonto eller sparekonto).
    """
    print(f"\n{BLUE_ITALIC}------------------ Velg Konto ------------------{RESET}")
    print(" 1. Brukskonto")
    print(" 2. Sparekonto")
    print(f"{BLUE_ITALIC}------------------------------------------------{RESET}")

    if action == "transfer_from":
        choice = input("Velg konto du vil overføre fra: ")
    elif action == "transfer_to":
        choice = input("Velg konto du vil overføre til: ")
    else:
        choice = input("Skriv inn tall for å velge konto: ")

    if choice == "1":
        return "brukskonto"
    elif choice == "2":
        return "sparekonto"
    else:
        input(f"{RED}Ugyldig valg! Vennligst velg et tall fra menyen (1-2). Trykk Enter for å prøve igjen{RESET}")
        return select_account_type(action)


# Start programmet ved å vise startmenyen
print_start_menu()