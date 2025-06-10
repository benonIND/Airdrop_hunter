# helpers.py
import os
import sqlite3
import time
from datetime import datetime

# Konfigurasi warna untuk terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Database setup
def setup_database():
    conn = sqlite3.connect('airdrop_hunter.db')
    c = conn.cursor()
    
    # Buat tabel untuk menyimpan airdrop yang disimpan
    c.execute('''CREATE TABLE IF NOT EXISTS saved_airdrops
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  value TEXT,
                  end_date TEXT,
                  source TEXT,
                  url TEXT,
                  added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Buat tabel untuk notifikasi
    c.execute('''CREATE TABLE IF NOT EXISTS notifications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  airdrop_id INTEGER,
                  notify_date TEXT,
                  notified INTEGER DEFAULT 0,
                  FOREIGN KEY(airdrop_id) REFERENCES saved_airdrops(id))''')
    
    conn.commit()
    conn.close()

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Fungsi untuk menampilkan banner
def show_banner():
    clear_screen()
    print(f"""{Colors.OKGREEN}
    █████╗ ██╗██████╗ ██████╗  ██████╗ ██████╗ 
    ██╔══██╗██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
    ███████║██║██████╔╝██████╔╝██║   ██║██████╔╝
    ██╔══██║██║██╔═══╝ ██╔═══╝ ██║   ██║██╔═══╝ 
    ██║  ██║██║██║     ██║     ╚██████╔╝██║     
    ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝      ╚═════╝ ╚═╝     
    {Colors.ENDC}""")
    print(f"{Colors.BOLD}=== Airdrop Hunter v2.0 ==={Colors.ENDC}")
    print(f"{Colors.WARNING}Developer: Yorima_ (github.com/benonIND){Colors.ENDC}\n")

# Fungsi untuk mendapatkan data dari database
def get_db_data(query, params=()):
    conn = sqlite3.connect('airdrop_hunter.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return [dict(row) for row in results]

# Fungsi untuk eksekusi query ke database
def execute_db_query(query, params=()):
    conn = sqlite3.connect('airdrop_hunter.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()
    
def format_table(headers, rows):
    """Format data menjadi tabel teks"""
    # Hitung lebar kolom
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Buat garis pembatas
    line = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    
    # Format header
    header_line = "|" + "|".join(
        [f" {header.ljust(col_widths[i])} " for i, header in enumerate(headers)]
    ) + "|"
    
    # Format baris data
    data_lines = []
    for row in rows:
        data_line = "|" + "|".join(
            [f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row)]
        ) + "|"
        data_lines.append(data_line)
    
    return "\n".join([line, header_line, line] + data_lines + [line])
