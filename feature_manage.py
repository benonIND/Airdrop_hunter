# feature_manage.py
# Berisi fungsi untuk mengelola status atau menghapus airdrop.

from utils import clear_screen, save_data

def manage_airdrops(data):
    """Mengelola status atau menghapus airdrop."""
    clear_screen()
    print("--- Kelola Airdrop ---")
    airdrops = data.get('airdrops', [])
    
    if not airdrops:
        print("Belum ada airdrop untuk dikelola.")
        input("\nTekan Enter untuk kembali...")
        return

    for i, airdrop in enumerate(airdrops):
        print(f"[{i}] {airdrop['name']} (Status: {airdrop['status']})")

    try:
        choice = int(input("\nPilih nomor airdrop (atau ketik angka lain untuk batal): "))
        if 0 <= choice < len(airdrops):
            a = airdrops[choice]
            print(f"\nPilihan: {a['name']}\n1. Tandai 'Selesai'\n2. Tandai 'Sedang Berjalan'\n3. Hapus\n4. Batal")
            action = input("Pilih tindakan (1-4): ")
            if action == '1': airdrops[choice]['status'] = 'completed'
            elif action == '2': airdrops[choice]['status'] = 'ongoing'
            elif action == '3':
                if input(f"Yakin hapus '{a['name']}'? (y/n): ").lower() == 'y':
                    data['airdrops'].pop(choice)
                    print("Airdrop telah dihapus.")
            save_data(data)
        else: print("Pilihan tidak valid.")
    except ValueError: print("Input tidak valid.")
    
    input("\nTekan Enter untuk kembali...")

