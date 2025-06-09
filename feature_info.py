# feature_info.py
# Berisi fungsi untuk menampilkan dan mengedit info pengguna.

from utils import clear_screen, save_data

def show_my_info(data):
    """Menampilkan informasi personal untuk copy-paste."""
    clear_screen()
    print("--- Informasi Saya (Untuk Copy-Paste) ---")
    info = data.get('my_info', {})
    if not any(info.values()):
        print("Informasi belum diatur. Silakan edit terlebih dahulu.")
    else:
        for key, value in info.items():
            print(f"-> {key.replace('_', ' ').title()}: {value}")
    input("\nTekan Enter untuk kembali ke menu...")

def edit_my_info(data):
    """Mengedit informasi personal (wallet, sosial media)."""
    clear_screen()
    print("--- Edit Informasi Saya ---")
    info = data['my_info']
    for key, value in info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\nMasukkan key yang ingin diubah (cth: eth_wallet) atau 'kembali' untuk batal:")
    key_to_edit = input("> ").lower()

    if key_to_edit in info:
        new_value = input(f"Masukkan nilai baru untuk {key_to_edit}: ")
        info[key_to_edit] = new_value
        save_data(data)
        print("\nInformasi berhasil diperbarui!")
    elif key_to_edit != 'kembali':
        print("\nKey tidak valid.")
    
    input("\nTekan Enter untuk kembali ke menu...")

