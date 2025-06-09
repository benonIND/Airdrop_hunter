# main.py
# File utama untuk menjalankan aplikasi Airdrop Helper.

# Mengimpor fungsi dari file-file fitur
from utils import load_data, clear_screen
from feature_view import view_airdrops
from feature_add import add_airdrop
from feature_manage import manage_airdrops
from feature_info import show_my_info, edit_my_info
from feature_search import search_new_airdrops

def print_header():
    """Mencetak header aplikasi dengan logo ASCII."""
    # Logo dan teks kustom
    logo = r"""
     __ __   ____  ____    ____  _   _  _  _  ____  ____     
    (  (  ) / ___)(  _ \  (  __)( )_( )( \/ )( ___)(  _ \    
    /    /  \___ \ )___/   ) _)  ) _ (  )  (  )__)  )   /    
    \_)__)  (____/(__)    (____)(_) (_)(_/\_)(____)(_)\_)___ 
     ____  _   _  _____  __  __  ____  _____   _   _  ____  
    ( ___)( )_( )(  _  )(  )(  )(  _ \(  _  ) ( )_( )/ ___) 
     )__)  ) _ (  )(_)(  )(__)(  )___/ )(_)(   ) _ ( \___ \ 
    (____)(_) (_)(_____)(______)(__)  (_____) (_) (_)(____/ 
    """
    
    # Warna untuk logo dan teks (menggunakan kode ANSI escape)
    # \033[96m untuk Cyan Terang, \033[93m untuk Kuning Terang, \033[0m untuk reset
    print("\033[96m" + logo + "\033[0m")
    print(" " * 23 + "\033[93m" + "--- by Yorima ---" + "\033[0m")
    print("-" * 65)


def main():
    """Fungsi utama untuk menjalankan menu."""
    data = load_data()
    
    while True:
        clear_screen()
        print_header() # Memanggil fungsi header baru

        # Tampilan Menu
        print("Menu:")
        print("1. Lihat Daftar Airdrop")
        print("2. Tambah Airdrop Baru")
        print("3. Kelola Airdrop (Ubah Status/Hapus)")
        print("4. Tampilkan Info Saya (untuk Copy-Paste)")
        print("5. Edit Info Saya")
        print("6. Cari Airdrop Baru (Otomatis)")
        print("7. Keluar")
        print("-" * 65)

        pilihan = input("Pilih menu (1-7): ")

        if pilihan == '1':
            view_airdrops(data)
        elif pilihan == '2':
            add_airdrop(data)
        elif pilihan == '3':
            manage_airdrops(data)
        elif pilihan == '4':
            show_my_info(data)
        elif pilihan == '5':
            edit_my_info(data)
        elif pilihan == '6':
            search_new_airdrops(data)
        elif pilihan == '7':
            print("\nTerima kasih telah menggunakan skrip ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()

