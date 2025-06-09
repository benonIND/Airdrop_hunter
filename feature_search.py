# feature_search.py
# Berisi fungsi untuk mencari airdrop baru secara otomatis.

import requests
import xml.etree.ElementTree as ET
from utils import clear_screen, AIRDROP_RSS_FEED

def search_new_airdrops(data):
    """Mencari airdrop baru dari RSS feed dan menampilkannya."""
    clear_screen()
    print(f"--- Mencari Airdrop Baru dari Sumber ---\nSumber: {AIRDROP_RSS_FEED}\n")
    print("Mohon tunggu, mengambil data...")

    try:
        response = requests.get(AIRDROP_RSS_FEED, timeout=15)
        response.raise_for_status()

        saved_links = {airdrop['link'] for airdrop in data['airdrops']}
        root = ET.fromstring(response.content)
        new_airdrops_found = []

        for item in root.findall('./channel/item'):
            title = item.find('title').text
            link = item.find('link').text
            
            if link not in saved_links:
                new_airdrops_found.append({'title': title, 'link': link})

        if not new_airdrops_found:
            print("\nTidak ada airdrop baru yang ditemukan saat ini.")
        else:
            print(f"\nBerhasil! Ditemukan {len(new_airdrops_found)} airdrop baru:")
            for i, airdrop in enumerate(new_airdrops_found, 1):
                print(f"{i}. {airdrop['title']}")
                print(f"   Link: {airdrop['link']}")

    except requests.exceptions.RequestException as e:
        print(f"\nError: Gagal mengambil data. Periksa koneksi internet Anda.")
    except ET.ParseError:
        print("\nError: Gagal memproses data dari sumber.")
    
    input("\nTekan Enter untuk kembali ke menu...")

