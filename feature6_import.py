# feature6_import.py
from helpers import Colors, execute_db_query, show_banner, clear_screen
import json
import csv
import os

def import_from_json():
    filename = input("Masukkan nama file JSON: ")
    if not os.path.exists(filename):
        print(f"{Colors.FAIL}File tidak ditemukan.{Colors.ENDC}")
        return
    
    try:
        with open(filename, 'r') as f:
            airdrops = json.load(f)
        
        for airdrop in airdrops:
            # Hindari impor duplikat
            existing = execute_db_query("SELECT * FROM saved_airdrops WHERE name = ?", (airdrop['name'],), fetch=True)
            if not existing:
                execute_db_query('''INSERT INTO saved_airdrops 
                                 (name, value, end_date, source, url) 
                                 VALUES (?, ?, ?, ?, ?)''',
                              (airdrop['name'], airdrop.get('value', 'N/A'), 
                               airdrop.get('end_date', 'N/A'), 
                               airdrop.get('source', 'Imported'), 
                               airdrop.get('url', '')))
        
        print(f"{Colors.OKGREEN}Berhasil mengimpor {len(airdrops)} airdrop!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error saat mengimpor: {e}{Colors.ENDC}")

def import_menu():
    show_banner()
    print(f"{Colors.BOLD}=== Impor Data Airdrop ==={Colors.ENDC}")
    print("1. Impor dari JSON")
    print("2. Kembali")
    
    choice = input("\nPilih opsi (1-2): ")
    
    if choice == '1':
        import_from_json()
    elif choice == '2':
        return
    else:
        print(f"{Colors.FAIL}Pilihan tidak valid.{Colors.ENDC}")
        time.sleep(1)
        import_menu()
        return
    
    input("\nTekan Enter untuk kembali...")