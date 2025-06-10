import requests
from bs4 import BeautifulSoup
from helpers import clear_screen, show_banner, Colors
import time
from shared_data import saved_airdrops

SCRAPINGBEE_API_KEY = "OIK50U81DREHG0CLIGCZ2SVRT1ZQIPNS9G3ZJQVE6HR85155GRWOVDH9E7VOTTW42359K5IG74V2C0EZ"  # Ganti dengan API key Anda

def fetch_with_scrapingbee(url):
    try:
        response = requests.get(
            f"https://app.scrapingbee.com/api/v1/?api_key={SCRAPINGBEE_API_KEY}&url={url}&render_js=false&premium_proxy=true"
        )
        if response.status_code == 200:
            return response
        print(f"{Colors.WARNING}ScrapingBee Error: Status {response.status_code}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}ScrapingBee Connection Error: {e}{Colors.ENDC}")
    return None

def fetch_coinmarketcap():
    try:
        url = "https://coinmarketcap.com/airdrop/"
        response = fetch_with_scrapingbee(url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = []
        
        for card in soup.select('div.sc-1snuar3-1.dVnPhT'):
            name = card.select_one('p.sc-1eb5slv-0.iworPT').text.strip()
            value = card.select_one('span.sc-1eb5slv-0.kZlTnE').text.strip()
            link = card.select_one('a.cmc-link')['href'] if card.select_one('a.cmc-link') else url
            
            airdrops.append({
                'name': name,
                'value': value,
                'end_date': "N/A",
                'source': 'CoinMarketCap',
                'url': f"https://coinmarketcap.com{link}"
            })
        
        return airdrops[:10]  # Batasi 10 hasil
    except Exception as e:
        print(f"{Colors.FAIL}CoinMarketCap Parsing Error: {e}{Colors.ENDC}")
        return []

def fetch_coingecko():
    try:
        url = "https://www.coingecko.com/en/airdrops"
        response = fetch_with_scrapingbee(url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        airdrops = []
        
        for row in soup.select('table tbody tr')[:10]:
            cols = row.select('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                value = cols[1].text.strip()
                end_date = cols[2].text.strip()
                link = cols[0].select_one('a')['href'] if cols[0].select_one('a') else url
                
                airdrops.append({
                    'name': name,
                    'value': value,
                    'end_date': end_date,
                    'source': 'CoinGecko',
                    'url': f"https://www.coingecko.com{link}"
                })
        
        return airdrops
    except Exception as e:
        print(f"{Colors.FAIL}CoinGecko Parsing Error: {e}{Colors.ENDC}")
        return []

def search_airdrops():
    show_banner()
    print(f"{Colors.BOLD}=== Pencarian Airdrop (ScrapingBee) ==={Colors.ENDC}")
    print("Mengambil data... (mungkin butuh 10-30 detik)")
    
    start_time = time.time()
    sources = [
        ("CoinMarketCap", fetch_coinmarketcap),
        ("CoinGecko", fetch_coingecko)
    ]
    
    airdrops = []
    for source_name, fetcher in sources:
        print(f"\n🔄 Mengambil dari {source_name}...")
        try:
            results = fetcher()
            if results:
                airdrops.extend(results)
                print(f"✅ Ditemukan {len(results)} airdrop")
            else:
                print(f"{Colors.WARNING}⚠ Tidak ada hasil{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error: {type(e).__name__}{Colors.ENDC}")
    
    elapsed = time.time() - start_time
    print(f"\n⌛ Selesai dalam {elapsed:.1f} detik")
    
    if not airdrops:
        print(f"\n{Colors.FAIL}Gagal mendapatkan data.{Colors.ENDC}")
        print(f"{Colors.WARNING}Pastikan:{Colors.ENDC}")
        print("- API Key ScrapingBee valid")
        print("- Kuota ScrapingBee mencukupi")
        input("\nTekan Enter untuk kembali...")
        return
    
    show_banner()
    print(f"{Colors.BOLD}=== Hasil Airdrop ({len(airdrops)} ditemukan) ==={Colors.ENDC}")
    
    for idx, airdrop in enumerate(airdrops[:15], 1):
        print(f"\n{Colors.OKBLUE}{idx}. {airdrop['name']}{Colors.ENDC}")
        print(f"   💰 Nilai: {airdrop['value']}")
        print(f"   📅 Deadline: {airdrop['end_date']}")
        print(f"   🌐 Sumber: {airdrop['source']}")
        print(f"   🔗 Detail: {airdrop['url']}")
    
    choice = input("\nPilih airdrop untuk disimpan (1-15) atau Enter untuk kembali: ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(airdrops):
            saved_airdrops.append(airdrops[idx])
            print(f"{Colors.OKGREEN}Berhasil disimpan!{Colors.ENDC}")
            time.sleep(1)
    
    input("\nTekan Enter untuk kembali...")
