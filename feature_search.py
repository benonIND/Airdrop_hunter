# feature_search_scraping.py
# Berisi fungsi untuk mencari airdrop baru menggunakan metode Web Scraping.

import requests
from bs4 import BeautifulSoup
from utils import clear_screen

# URL target yang akan kita "scrape"
TARGET_URL = "https://airdrops.io/latest/"

def search_new_airdrops(data):
    """Mencari airdrop baru dengan mengambil data langsung dari airdrops.io."""
    clear_screen()
    print(f"--- Mencari Airdrop Baru (Metode Scraping) ---\nSumber: {TARGET_URL}\n")
    print("Mohon tunggu, mengambil dan memproses halaman web...")

    try:
        # Menambahkan 'User-Agent' sangat penting agar tidak langsung diblokir
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(TARGET_URL, headers=headers, timeout=20)
        response.raise_for_status()

        # Menggunakan BeautifulSoup untuk mem-parsing HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # Mencari semua airdrop. Berdasarkan inspeksi web, setiap airdrop ada di dalam
        # tag <article> dengan class 'air-post'. Ini bisa berubah jika web di-update.
        latest_airdrops = soup.find_all('article', class_='air-post')

        if not latest_airdrops:
            print("\nTidak dapat menemukan daftar airdrop. Mungkin struktur web telah berubah.")
            input("\nTekan Enter untuk kembali...")
            return

        print(f"\nBerhasil! Ditemukan {len(latest_airdrops)} airdrop terbaru:\n")
        
        saved_links = {airdrop['link'] for airdrop in data['airdrops']}
        new_airdrops_found = 0

        for airdrop_html in latest_airdrops:
            title_element = airdrop_html.find('h3')
            link = title_element.a['href']
            
            # Cek apakah link sudah disimpan
            if link not in saved_links:
                new_airdrops_found += 1
                title = title_element.text.strip()
                
                # Mengambil data ekstra: deskripsi singkat
                meta_div = airdrop_html.find('div', class_='air-post-meta')
                description = meta_div.text.strip().replace('\n', ' | ')

                print(f"✅ {title}")
                print(f"   Info: {description}")
                print(f"   Link: {link}\n")
        
        if new_airdrops_found == 0:
            print("Tidak ada airdrop baru yang ditemukan saat ini (semua sudah tersimpan).")

    except requests.exceptions.RequestException as e:
        print(f"\nError: Gagal mengambil data. Periksa koneksi internet atau URL mungkin salah.")
    except Exception as e:
        print(f"\nTerjadi error saat memproses data: {e}")
    
    input("\nTekan Enter untuk kembali ke menu...")

