#!/usr/bin/env python3
# Airdrop Hunter - Main File
# Developer: Yorima_ (github.com/yorima-dev)

import os
import sys
from helpers import clear_screen, show_banner, setup_database, Colors

# Import semua fitur
from feature1_search import search_airdrops
from feature2_save import save_airdrop_menu, view_saved_airdrops
from feature3_notify import set_notification, check_notifications
from feature4_category import search_by_category
from feature5_export import export_menu
from feature6_import import import_menu
from feature7_stats import show_stats

def main_menu():
    setup_database()
    
    while True:
        clear_screen()
        show_banner()
        print(f"{' MENU UTAMA ':=^50}")
        print("1. 🔍 Cari Airdrop Terbaru")
        print("2. 💾 Simpan Airdrop Favorit")
        print("3. 🔔 Kelola Notifikasi")
        print("4. 🗂️ Cari Berdasarkan Kategori")
        print("5. 📤 Ekspor Data Airdrop")
        print("6. 📥 Impor Data Airdrop")
        print("7. 📊 Statistik Airdrop")
        print("8. 🚪 Keluar")
        
        choice = input("\nPilih menu (1-8): ")
        
        if choice == '1':
            search_airdrops()
        elif choice == '2':
            save_airdrop_menu()
        elif choice == '3':
            manage_notifications()
        elif choice == '4':
            search_by_category()
        elif choice == '5':
            export_menu()
        elif choice == '6':
            import_menu()
        elif choice == '7':
            show_stats()
        elif choice == '8':
            clear_screen()
            print("Terima kasih telah menggunakan Airdrop Hunter!")
            print("Developer: Yorima_ (github.com/yorima-dev)")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(1)

def manage_notifications():
    while True:
        clear_screen()
        show_banner()
        print(f"{' KELOLA NOTIFIKASI ':=^50}")
        print("1. Set Notifikasi Baru")
        print("2. Cek Notifikasi Aktif")
        print("3. Kembali")
        
        choice = input("\nPilih menu (1-3): ")
        
        if choice == '1':
            set_notification()
        elif choice == '2':
            check_notifications()
        elif choice == '3':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            time.sleep(1)

if __name__ == "__main__":
    # Cek dependensi (hapus matplotlib)
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Menginstall dependensi yang diperlukan...")
        os.system('pip install requests beautifulsoup4')
    
    main_menu()
