# feature4_category.py
from helpers import Colors, show_banner, clear_screen
from feature1_search import fetch_coinmarketcap_airdrops, fetch_coingecko_airdrops, fetch_airdrops_io
import time

def search_high_value():
    show_banner()
    print(f"{Colors.BOLD}=== Airdrop Nilai Tertinggi ==={Colors.ENDC}")
    print("Fitur ini dalam pengembangan...")
    time.sleep(2)

def search_near_deadline():
    show_banner()
    print(f"{Colors.BOLD}=== Airdrop Deadline Terdekat ==={Colors.ENDC}")
    print("Fitur ini dalam pengembangan...")
    time.sleep(2)

def search_by_source():
    show_banner()
    print(f"{Colors.BOLD}=== Pencarian Berdasarkan Sumber ==={Colors.ENDC}")
    print("1. CoinMarketCap")
    print("2. CoinGecko")
    print("3. Airdrops.io")
    print("4. Kembali")
    
    choice = input("\nPilih sumber (1-4): ")
    
    if choice == '1':
        airdrops = fetch_coinmarketcap_airdrops()
        source = "CoinMarketCap"
    elif choice == '2':
        airdrops = fetch_coingecko_airdrops()
        source = "CoinGecko"
    elif choice == '3':
        airdrops = fetch_airdrops_io()
        source = "Airdrops.io"
    elif choice == '4':
        return
    else:
        print(f"{Colors.FAIL}Pilihan tidak valid.{Colors.ENDC}")
        time.sleep(1)
        search_by_source()
        return
    
    show_banner()
    print(f"{Colors.BOLD}=== Hasil dari {source} ==={Colors.ENDC}")
    
    if not airdrops:
        print(f"{Colors.WARNING}Tidak menemukan airdrop dari sumber ini.{Colors.ENDC}")
    else:
        for idx, airdrop in enumerate(airdrops, 1):
            print(f"\n{Colors.OKBLUE}{idx}. {airdrop['name']}{Colors.ENDC}")
            print(f"   💰 Nilai: {airdrop['value']}")
            print(f"   📅 Tanggal Berakhir: {airdrop['end_date']}")
            print(f"   🔗 URL: {airdrop['url']}")
    
    input("\nTekan Enter untuk kembali...")

def search_by_category():
    while True:
        show_banner()
        print(f"{Colors.BOLD}=== Pencarian Berdasarkan Kategori ==={Colors.ENDC}")
        print("1. Nilai Tertinggi")
        print("2. Deadline Terdekat")
        print("3. Sumber Tertentu")
        print("4. Kembali")
        
        choice = input("\nPilih kategori (1-4): ")
        
        if choice == '1':
            search_high_value()
        elif choice == '2':
            search_near_deadline()
        elif choice == '3':
            search_by_source()
        elif choice == '4':
            break
        else:
            print(f"{Colors.FAIL}Pilihan tidak valid.{Colors.ENDC}")
            time.sleep(1)