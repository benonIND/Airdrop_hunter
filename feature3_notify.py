# feature3_notify.py
from helpers import Colors, get_db_data, execute_db_query, show_banner, clear_screen
from datetime import datetime
import time

def set_notification():
    from feature2_save import view_saved_airdrops
    saved_airdrops = view_saved_airdrops()
    
    if not saved_airdrops:
        input("\nTekan Enter untuk kembali...")
        return
    
    airdrop_id = input("\nMasukkan ID airdrop untuk set notifikasi: ")
    if not airdrop_id.isdigit():
        print(f"{Colors.FAIL}ID harus berupa angka.{Colors.ENDC}")
        time.sleep(1)
        return
    
    notify_date = input("Masukkan tanggal notifikasi (YYYY-MM-DD): ")
    try:
        datetime.strptime(notify_date, '%Y-%m-%d')
    except ValueError:
        print(f"{Colors.FAIL}Format tanggal tidak valid. Gunakan YYYY-MM-DD.{Colors.ENDC}")
        time.sleep(1)
        return
    
    # Cek apakah airdrop ada
    airdrop = get_db_data("SELECT * FROM saved_airdrops WHERE id = ?", (airdrop_id,))
    if not airdrop:
        print(f"{Colors.FAIL}Airdrop dengan ID tersebut tidak ditemukan.{Colors.ENDC}")
        time.sleep(1)
        return
    
    # Simpan notifikasi
    execute_db_query('''INSERT INTO notifications 
                     (airdrop_id, notify_date) 
                     VALUES (?, ?)''',
                  (airdrop_id, notify_date))
    
    print(f"{Colors.OKGREEN}Notifikasi berhasil diset!{Colors.ENDC}")
    time.sleep(1)

def check_notifications(silent=False):
    today = datetime.now().strftime('%Y-%m-%d')
    notifications = get_db_data('''SELECT n.id, n.notify_date, a.name, a.url 
                                  FROM notifications n
                                  JOIN saved_airdrops a ON n.airdrop_id = a.id
                                  WHERE n.notified = 0 AND n.notify_date <= ?''', 
                               (today,))
    
    if notifications and not silent:
        show_banner()
        print(f"{Colors.BOLD}=== NOTIFIKASI AIRDROP ==={Colors.ENDC}")
        for notif in notifications:
            print(f"\n{Colors.WARNING}⏰ WAKTUNYA UNTUK AIRDROP!{Colors.ENDC}")
            print(f"   📛 Nama: {notif['name']}")
            print(f"   📅 Tanggal Notifikasi: {notif['notify_date']}")
            print(f"   🔗 URL: {notif['url']}")
        
        # Tandai notifikasi sebagai telah diberitahu
        for notif in notifications:
            execute_db_query("UPDATE notifications SET notified = 1 WHERE id = ?", (notif['id'],))
        
        input("\nTekan Enter untuk melanjutkan...")
    
    return notifications