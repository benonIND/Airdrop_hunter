# feature5_export.py
from helpers import Colors, get_db_data, show_banner, clear_screen
import json
import csv
from datetime import datetime

def export_to_json():
    saved_airdrops = get_db_data("SELECT * FROM saved_airdrops")
    
    if not saved_airdrops:
        print(f"{Colors.WARNING}Tidak ada data airdrop untuk diekspor.{Colors.ENDC}")
        return
    
    filename = f"airdrop_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(saved_airdrops, f, indent=4)
    
    print(f"{Colors.OKGREEN}Data berhasil diekspor ke {filename}{Colors.ENDC}")

def export_to_csv():
    saved_airdrops = get_db_data("SELECT * FROM saved_airdrops")
    
    if not saved_airdrops:
        print(f"{Colors.WARNING}Tidak ada data airdrop untuk diekspor.{Colors.ENDC}")
        return
    
    filename = f"airdrop_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=saved_airdrops[0].keys())
        writer.writeheader()
        writer.writerows(saved_airdrops)
    
    print(f"{Colors.OKGREEN}Data berhasil diekspor ke {filename}{Colors.ENDC}")

def export_menu():
    show_banner()
    print(f"{Colors.BOLD}=== Ekspor Data Airdrop ==={Colors.ENDC}")
    print("1. Ekspor ke JSON")
    print("2. Ekspor ke CSV")
    print("3. Kembali")
    
    choice = input("\nPilih format ekspor (1-3): ")
    
    if choice == '1':
        export_to_json()
    elif choice == '2':
        export_to_csv()
    elif choice == '3':
        return
    else:
        print(f"{Colors.FAIL}Pilihan tidak valid.{Colors.ENDC}")
        time.sleep(1)
        export_menu()
        return
    
    input("\nTekan Enter untuk kembali...")