from helpers import Colors, show_banner, clear_screen, format_table
from feature1_search import fetch_with_scrapingbee, SCRAPINGBEE_API_KEY
import time
import random
from datetime import datetime

def fetch_by_source(source):
    """Fungsi terpusat untuk semua sumber"""
    if source == "CoinMarketCap":
        return fetch_coinmarketcap()
    elif source == "CoinGecko":
        return fetch_coingecko()
    elif source == "AirdropAlert":
        return fetch_airdropalert()
    return []

def fetch_coinmarketcap():
    try:
        url = "https://coinmarketcap.com/airdrop/"
        response = fetch_with_scrapingbee(url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        return [{
            'name': card.select_one('p.sc-1eb5slv-0.iworPT').text.strip(),
            'value': card.select_one('span.sc-1eb5slv-0.kZlTnE').text.strip(),
            'end_date': "N/A",
            'source': 'CoinMarketCap',
            'url': f"https://coinmarketcap.com{card.select_one('a.cmc-link')['href']}"
        } for card in soup.select('div.sc-1snuar3-1.dVnPhT')[:10]]
    except Exception as e:
        print(f"{Colors.FAIL}CoinMarketCap Error: {e}{Colors.ENDC}")
        return []

def fetch_coingecko():
    try:
        url = "https://www.coingecko.com/en/airdrops"
        response = fetch_with_scrapingbee(url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        return [{
            'name': cols[0].text.strip(),
            'value': cols[1].text.strip(),
            'end_date': cols[2].text.strip(),
            'source': 'CoinGecko',
            'url': f"https://www.coingecko.com{cols[0].select_one('a')['href']}"
        } for row in soup.select('table tbody tr')[:10] 
          if len(cols := row.select('td')) >= 3]
    except Exception as e:
        print(f"{Colors.FAIL}CoinGecko Error: {e}{Colors.ENDC}")
        return []

def fetch_airdropalert():
    try:
        url = "https://airdropalert.com"
        response = fetch_with_scrapingbee(url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        return [{
            'name': card.select_one('h3.airdrop-name').text.strip(),
            'value': card.select_one('span.airdrop-value').text.strip(),
            'end_date': card.select_one('div.airdrop-end-date').text.strip(),
            'source': 'AirdropAlert',
            'url': url + card.select_one('a')['href']
        } for card in soup.select('div.airdrop-card:not(.expired)')[:10]]
    except Exception as e:
        print(f"{Colors.FAIL}AirdropAlert Error: {e}{Colors.ENDC}")
        return []

def search_by_value_range(min_value=1000):
    show_banner()
    print(f"{Colors.BOLD}=== Airdrop Bernilai > ${min_value} ===")
    
    all_airdrops = []
    for source in ["CoinMarketCap", "CoinGecko", "AirdropAlert"]:
        all_airdrops.extend(fetch_by_source(source))
    
    filtered = []
    for airdrop in all_airdrops:
        try:
            # Ekstrak nilai numerik dari string (contoh: "$1,000" -> 1000)
            value_str = airdrop['value'].replace('$', '').replace(',', '')
            if 'ETH' in value_str:
                value = float(value_str.replace('ETH', '')) * 3000  # Asumsi 1 ETH = $3000
            else:
                value = float(value_str)
                
            if value >= min_value:
                filtered.append(airdrop)
        except:
            continue
    
    if not filtered:
        print(f"\n{Colors.WARNING}Tidak ditemukan airdrop > ${min_value}{Colors.ENDC}")
        input("\nTekan Enter untuk kembali...")
        return
    
    print(f"\n🔍 Ditemukan {len(filtered)} airdrop bernilai tinggi:")
    print(format_table(
        ["No", "Nama", "Nilai", "Sumber"],
        [[idx+1, a['name'], a['value'], a['source']] 
        for idx, a in enumerate(filtered([:15]))
    
    input("\nTekan Enter untuk kembali...")

def search_by_deadline(days=7):
    show_banner()
    print(f"{Colors.BOLD}=== Airdrop Berakhir dalam {days} Hari ===")
    
    all_airdrops = []
    for source in ["CoinGecko", "AirdropAlert"]:  # CoinMarketCap biasanya tidak ada end_date
        all_airdrops.extend(fetch_by_source(source))
    
    filtered = []
    today = datetime.now()
    
    for airdrop in all_airdrops:
        try:
            end_date = datetime.strptime(airdrop['end_date'], '%Y-%m-%d')
            if 0 <= (end_date - today).days <= days:
                filtered.append(airdrop)
        except:
            continue
    
    if not filtered:
        print(f"\n{Colors.WARNING}Tidak ada airdrop berakhir dalam {days} hari{Colors.ENDC}")
        input("\nTekan Enter untuk kembali...")
        return
    
    print(f"\n⏳ Airdrop segera berakhir:")
    print(format_table(
        ["No", "Nama", "Deadline", "Sumber"],
        [[idx+1, a['name'], a['end_date'], a['source']] 
        for idx, a in enumerate(filtered[:15]))
    
    input("\nTekan Enter untuk kembali...")

def search_by_category():
    while True:
        show_banner()
        print(f"{Colors.BOLD}=== Pencarian Berdasarkan Kategori ===")
        print("1. 🔍 Berdasarkan Sumber")
        print("2. 💰 Nilai Tertinggi (>$1000)")
        print("3. ⏳ Deadline Terdekat (7 hari)")
        print("4. 🏠 Kembali ke Menu Utama")
        
        choice = input("\nPilih kategori (1-4): ")
        
        if choice == '1':
            search_by_source_menu()
        elif choice == '2':
            search_by_value_range(1000)
        elif choice == '3':
            search_by_deadline(7)
        elif choice == '4':
            break
        else:
            print(f"{Colors.FAIL}Pilihan tidak valid!{Colors.ENDC}")
            time.sleep(1)

def search_by_source_menu():
    while True:
        show_banner()
        print(f"{Colors.BOLD}=== Pilih Sumber ===")
        print("1. CoinMarketCap")
        print("2. CoinGecko")
        print("3. AirdropAlert")
        print("4. Kembali")
        
        choice = input("\nPilih sumber (1-4): ")
        
        sources = {
            '1': ("CoinMarketCap", fetch_coinmarketcap),
            '2': ("CoinGecko", fetch_coingecko),
            '3': ("AirdropAlert", fetch_airdropalert)
        }
        
        if choice in sources:
            source_name, fetcher = sources[choice]
            show_results_from_source(source_name, fetcher)
        elif choice == '4':
            break
        else:
            print(f"{Colors.FAIL}Pilihan tidak valid!{Colors.ENDC}")
            time.sleep(1)

def show_results_from_source(source_name, fetcher):
    show_banner()
    print(f"{Colors.BOLD}=== Hasil dari {source_name} ===")
    print(f"Mengambil data...")
    
    try:
        airdrops = fetcher()
        if not airdrops:
            print(f"\n{Colors.WARNING}Tidak ada data dari {source_name}{Colors.ENDC}")
            input("\nTekan Enter untuk kembali...")
            return
        
        print(f"\n✅ Ditemukan {len(airdrops)} airdrop:")
        print(format_table(
            ["No", "Nama", "Nilai", "Deadline"],
            [[idx+1, a['name'], a['value'], a['end_date']] 
            for idx, a in enumerate(airdrops[:15])))
        
        input("\nTekan Enter untuk kembali...")
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        input("\nTekan Enter untuk kembali...")
