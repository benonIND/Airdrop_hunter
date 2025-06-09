# feature_add.py
# Berisi fungsi untuk menambah airdrop baru.

from utils import clear_screen, save_data

def add_airdrop(data):
    """Menambahkan entri airdrop baru."""
    clear_screen()
    print("--- Tambah Airdrop Baru ---")
    name = input("Nama Project Airdrop: ")
    link = input("Link Airdrop (Gleam/Website/dll): ")
    
    airdrop = {
        "name": name,
        "link": link,
        "status": "ongoing"
    }
    
    data['airdrops'].append(airdrop)
    save_data(data)
    print(f"\nAirdrop '{name}' berhasil ditambahkan!")
    input("\nTekan Enter untuk kembali ke menu...")

