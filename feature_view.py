# feature_view.py
# Berisi fungsi untuk melihat daftar airdrop yang tersimpan.

from utils import clear_screen

def view_airdrops(data):
    """Melihat daftar airdrop yang tersimpan."""
    clear_screen()
    print("--- Daftar Airdrop ---")
    airdrops = data.get('airdrops', [])
    
    if not airdrops:
        print("Belum ada airdrop yang disimpan.")
    else:
        ongoing = [a for a in airdrops if a['status'] == 'ongoing']
        completed = [a for a in airdrops if a['status'] == 'completed']

        if ongoing:
            print("\n[ SEDANG BERJALAN ]")
            for i, a in enumerate(ongoing, 1):
                print(f"{i}. {a['name']} - Status: {a['status'].title()}\n   Link: {a['link']}")
        
        if completed:
            print("\n[ SELESAI ]")
            for i, a in enumerate(completed, 1):
                print(f"{i}. {a['name']} - Status: {a['status'].title()}\n   Link: {a['link']}")

    input("\nTekan Enter untuk kembali ke menu...")

