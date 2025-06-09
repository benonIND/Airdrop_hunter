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
    """Mencetak header aplikasi dengan desain satu baris yang minimalis."""
    
    # Warna: \033[92m Hijau, \033[90m Abu-abu, \033[95m Magenta, \033[0m Reset
    green = "\033[92m"
    gray = "\033[90m"
    magenta = "\033[95m"
    reset = "\033[0m"

    # Desain header satu baris
    print(f"{green}»»--- {reset}Airdrop Hunter {gray}|{magenta} by Yorima{green} ---««{reset}\n")


def main():
    """Fungsi utama untuk menjalankan menu."""
    data = load_data()
    
    while True:
        clear_screen()
        print_header() # Memanggil fungsi header baru

        # Tampilan Menu
        gray = "\033[90m"
        reset = "\033[0m"

        print(f"1. Lihat Airdrop")
        print(f"2. Tambah Airdrop")
        print(f"3. Kelola Airdrop")
        print(f"4. Info Saya")
        print(f"5. Edit Info")
        print(f"6. Cari Airdrop Baru")
        print(f"7. Keluar")
        print(f"{gray}-----------------------------{reset}")

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

