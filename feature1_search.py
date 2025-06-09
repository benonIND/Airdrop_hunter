# feature1_search.py
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from helpers import clear_screen, show_banner, Colors, get_db_data, execute_db_query
import time

def fetch_coinmarketcap_airdrops():
    try:
        url = "https://coinmarketcap.com/airdrop/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        items = soup.find_all('div', class_='sc-1snuar3-1')
        
        for item in items[:10]:
            name_elem = item.find('p', class_='sc-1eb5slv-0')
            value_elem = item.find('span', class_='sc-1eb5slv-0')
            
            name = name_elem.text if name_elem else "N/A"
            value = value_elem.text if value_elem else "N/A"
            
            airdrops.append({
                'name': name,
                'value': value,
                'end_date': "N/A",
                'source': 'CoinMarketCap',
                'url': url
            })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from CoinMarketCap: {e}{Colors.ENDC}")
        return []

def fetch_coingecko_airdrops():
    try:
        url = "https://www.coingecko.com/en/airdrops"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        table = soup.find('tbody')
        if table:
            rows = table.find_all('tr')[:10]
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    name = cols[0].text.strip()
                    value = cols[1].text.strip()
                    end_date = cols[2].text.strip()
                    
                    airdrops.append({
                        'name': name,
                        'value': value,
                        'end_date': end_date,
                        'source': 'CoinGecko',
                        'url': url
                    })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from CoinGecko: {e}{Colors.ENDC}")
        return []

def fetch_airdrops_io():
    try:
        url = "https://airdrops.io/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        airdrops = []
        cards = soup.find_all('div', class_='airdrop-card')[:10]
        
        for card in cards:
            name_elem = card.find('h3')
            value_elem = card.find('div', class_='airdrop-value')
            end_date_elem = card.find('div', class_='airdrop-end-date')
            
            name = name_elem.text.strip() if name_elem else "N/A"
            value = value_elem.text.strip() if value_elem else "N/A"
            end_date = end_date_elem.text.strip() if end_date_elem else "N/A"
            
            airdrops.append({
                'name': name,
                'value': value,
                'end_date': end_date,
                'source': 'Airdrops.io',
                'url': url
            })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}Error fetching from Airdrops.io: {e}{Colors.ENDC}")
        return []

def search_airdrops():
    show_banner()
    print(f"{Colors.BOLD}=== Pencarian Airdrop Terbaru ==={Colors.ENDC}")
    print("Mengambil data dari berbagai sumber...")
    
    with ThreadPoolExecutor() as executor:
        cmc_future = executor.submit(fetch_coinmarketcap_airdrops)
        cg_future = executor.submit(fetch_coingecko_airdrops)
        ai_future = executor.submit(fetch_airdrops_io)
        
        airdrops = cmc_future.result() + cg_future.result() + ai_future.result()
    
    if not airdrops:
        print(f"{Colors.WARNING}Tidak menemukan airdrop dari sumber manapun.{Colors.ENDC}")
        input("\nTekan Enter untuk kembali...")
        return
    
    show_banner()
    print(f"{Colors.BOLD}=== Hasil Pencarian Airdrop ==={Colors.ENDC}")
    
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
            from feature2_save import save_airdrop
            save_airdrop(airdrops[idx])
            print(f"{Colors.OKGREEN}Airdrop berhasil disimpan!{Colors.ENDC}")
            time.sleep(1)
    
    input("\nTekan Enter untuk kembali ke menu utama...")