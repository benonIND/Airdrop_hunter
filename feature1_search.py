# feature1_search.py (Revisi)
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from helpers import clear_screen, show_banner, Colors
import time
from shared_data import saved_airdrops
import random

# Daftar User-Agent untuk menghindari blokir
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def fetch_coinmarketcap_airdrops():
    try:
        url = "https://coinmarketcap.com/airdrop/"
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        # Perbaikan: Gunakan selector yang lebih umum
        cards = soup.select('div.sc-1snuar3-1.dVnPhT')
        
        for card in cards[:10]:
            name_elem = card.select_one('p.sc-1eb5slv-0.iworPT')
            value_elem = card.select_one('span.sc-1eb5slv-0.kZlTnE')
            
            name = name_elem.text.strip() if name_elem else "N/A"
            value = value_elem.text.strip() if value_elem else "N/A"
            
            # Cari link detail
            link_elem = card.select_one('a.cmc-link')
            detail_url = f"https://coinmarketcap.com{link_elem['href']}" if link_elem else url
            
            airdrops.append({
                'name': name,
                'value': value,
                'end_date': "N/A",
                'source': 'CoinMarketCap',
                'url': detail_url
            })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from CoinMarketCap: {e}{Colors.ENDC}")
        return []

def fetch_coingecko_airdrops():
    try:
        url = "https://www.coingecko.com/en/airdrops"
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        table = soup.select_one('table[data-target="airdrops.table"]')
        
        if table:
            rows = table.select('tbody tr')[:10]
            
            for row in rows:
                cols = row.select('td')
                if len(cols) >= 3:
                    name = cols[0].text.strip()
                    value = cols[1].text.strip()
                    end_date = cols[2].text.strip()
                    
                    # Cari link detail
                    link_elem = cols[0].select_one('a')
                    detail_url = f"https://www.coingecko.com{link_elem['href']}" if link_elem else url
                    
                    airdrops.append({
                        'name': name,
                        'value': value,
                        'end_date': end_date,
                        'source': 'CoinGecko',
                        'url': detail_url
                    })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from CoinGecko: {e}{Colors.ENDC}")
        return []

def fetch_airdrops_io():
    try:
        url = "https://airdrops.io/"
        headers = get_random_headers()
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        cards = soup.select('div.airdrop-card')[:10]
        
        for card in cards:
            name_elem = card.select_one('h3.airdrop-name')
            value_elem = card.select_one('div.airdrop-value')
            end_date_elem = card.select_one('div.airdrop-end-date')
            
            name = name_elem.text.strip() if name_elem else "N/A"
            value = value_elem.text.strip() if value_elem else "N/A"
            end_date = end_date_elem.text.strip() if end_date_elem else "N/A"
            
            # Cari link detail
            link_elem = card.select_one('a.airdrop-link')
            detail_url = link_elem['href'] if link_elem else url
            
            airdrops.append({
                'name': name,
                'value': value,
                'end_date': end_date,
                'source': 'Airdrops.io',
                'url': detail_url
            })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from Airdrops.io: {e}{Colors.ENDC}")
        return []

def search_airdrops():
    show_banner()
    print(f"{Colors.BOLD}=== Pencarian Airdrop Terbaru ==={Colors.ENDC}")
    print("Mengambil data dari berbagai sumber... (mungkin butuh waktu)")
    
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            cmc_future = executor.submit(fetch_coinmarketcap_airdrops)
            cg_future = executor.submit(fetch_coingecko_airdrops)
            ai_future = executor.submit(fetch_airdrops_io)
            
            airdrops = []
            
            # Tambahkan timeout untuk setiap sumber
            for future in [cmc_future, cg_future, ai_future]:
                try:
                    result = future.result(timeout=15)
                    if result:
                        airdrops.extend(result)
                except Exception as e:
                    print(f"{Colors.WARNING}Peringatan: {e}{Colors.ENDC}")
    
    except Exception as e:
        print(f"{Colors.FAIL}Error dalam proses pencarian: {e}{Colors.ENDC}")
        airdrops = []
    
    if not airdrops:
        print(f"{Colors.WARNING}Tidak menemukan airdrop dari sumber manapun.{Colors.ENDC}")
        print(f"{Colors.WARNING}Kemungkinan penyebab:{Colors.ENDC}")
        print("- Website sumber memblokir akses")
        print("- Struktur website berubah")
        print("- Koneksi internet bermasalah")
        print(f"\n{Colors.OKBLUE}Silakan coba lagi nanti atau gunakan VPN.{Colors.ENDC}")
        input("\nTekan Enter untuk kembali...")
        return
    
    show_banner()
    print(f"{Colors.BOLD}=== Hasil Pencarian Airdrop ==={Colors.ENDC}")
    print(f"Ditemukan {len(airdrops)} airdrop dari berbagai sumber\n")
    
    for idx, airdrop in enumerate(airdrops, 1):
        print(f"\n{Colors.OKBLUE}{idx}. {airdrop['name']}{Colors.ENDC}")
        print(f"   💰 Nilai: {airdrop['value']}")
        print(f"   📅 Tanggal Berakhir: {airdrop['end_date']}")
        print(f"   🌐 Sumber: {airdrop['source']}")
        print(f"   🔗 URL: {airdrop['url']}")
    
    choice = input("\nPilih airdrop untuk disimpan (ketik nomor) atau Enter untuk kembali: ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(airdrops):
            saved_airdrops.append(airdrops[idx])
            print(f"{Colors.OKGREEN}Airdrop berhasil disimpan!{Colors.ENDC}")
            time.sleep(1)
    
    input("\nTekan Enter untuk kembali ke menu utama...")
