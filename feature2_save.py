# feature2_save.py
from helpers import Colors, get_db_data, execute_db_query, show_banner, clear_screen
import time

def save_airdrop(airdrop):
    query = '''INSERT INTO saved_airdrops 
               (name, value, end_date, source, url) 
               VALUES (?, ?, ?, ?, ?)'''
    params = (
        airdrop['name'],
        airdrop['value'],
        airdrop['end_date'],
        airdrop['source'],
        airdrop['url']
    )
    execute_db_query(query, params)

def view_saved_airdrops():
    query = "SELECT * FROM saved_airdrops ORDER BY added_date DESC"
    saved_airdrops = get_db_data(query)
    
    show_banner()
    print(f"{Colors.BOLD}=== Airdrop Tersimpan ==={Colors.ENDC}")
    
    if not saved_airdrops:
        print(f"{Colors.WARNING}Tidak ada airdrop yang tersimpan.{Colors.ENDC}")
    else:
        for airdrop in saved_airdrops:
            print(f"\n{Colors.OKBLUE}{airdrop['id']}. {airdrop['name']}{Colors.ENDC}")
            print(f"   💰 Nilai: {airdrop['value']}")
            print(f"   📅 Tanggal Berakhir: {airdrop['end_date']}")
            print(f"   🌐 Sumber: {airdrop['source']}")
            print(f"   🔗 URL: {airdrop['url']}")
            print(f"   ⏱️ Disimpan pada: {airdrop['added_date']}")
    
    return saved_airdrops

def save_airdrop_menu():
    saved_airdrops = view_saved_airdrops()
    
    if saved_airdrops:
        choice = input("\nMasukkan ID airdrop untuk dihapus atau Enter untuk kembali: ")
        if choice.isdigit():
            airdrop_id = int(choice)
            # Cek apakah ID valid
            ids = [a['id'] for a in saved_airdrops]
            if airdrop_id in ids:
                execute_db_query("DELETE FROM saved_airdrops WHERE id = ?", (airdrop_id,))
                execute_db_query("DELETE FROM notifications WHERE airdrop_id = ?", (airdrop_id,))
                print(f"{Colors.OKGREEN}Airdrop berhasil dihapus!{Colors.ENDC}")
                time.sleep(1)
    
    input("\nTekan Enter untuk kembali ke menu utama...")