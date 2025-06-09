# feature7_stats.py (Revisi)
from helpers import Colors, show_banner, clear_screen, format_table
from main import saved_airdrops
from datetime import datetime

def show_stats():
    show_banner()
    print(f"{Colors.BOLD}=== Statistik Airdrop ==={Colors.ENDC}")
    
    total = len(saved_airdrops)
    print(f"📊 Total Airdrop Tersimpan: {total}")
    
    if total == 0:
        input("\nTekan Enter untuk kembali...")
        return
    
    # Hitung statistik per sumber
    sources = {}
    for airdrop in saved_airdrops:
        source = airdrop.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    # Format tabel
    headers = ["Sumber", "Jumlah", "Persentase"]
    rows = []
    for source, count in sources.items():
        percentage = (count / total) * 100
        rows.append([
            source, 
            count, 
            f"{percentage:.1f}%"
        ])
    
    # Tambahkan baris total
    rows.append(["TOTAL", total, "100%"])
    
    print("\n🔢 Distribusi Berdasarkan Sumber:")
    print(format_table(headers, rows))
    
    # Hitung statistik berdasarkan waktu
    print("\n⏱️ Distribusi Berdasarkan Waktu Penyimpanan:")
    
    # Kelompokkan berdasarkan hari (dalam 7 hari terakhir)
    time_groups = {"Hari Ini": 0, "Kemarin": 0, "2-7 Hari": 0, ">1 Minggu": 0}
    today = datetime.now().date()
    
    for airdrop in saved_airdrops:
        added_date = datetime.strptime(airdrop.get('added_date', today.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        delta = (today - added_date).days
        
        if delta == 0:
            time_groups["Hari Ini"] += 1
        elif delta == 1:
            time_groups["Kemarin"] += 1
        elif 2 <= delta <= 7:
            time_groups["2-7 Hari"] += 1
        else:
            time_groups[">1 Minggu"] += 1
    
    # Format tabel waktu
    time_headers = ["Periode", "Jumlah", "Persentase"]
    time_rows = []
    for period, count in time_groups.items():
        percentage = (count / total) * 100 if total > 0 else 0
        time_rows.append([
            period, 
            count, 
            f"{percentage:.1f}%"
        ])
    
    print(format_table(time_headers, time_rows))
    
    input("\nTekan Enter untuk kembali...")