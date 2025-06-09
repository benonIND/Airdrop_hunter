# utils.py
# Berisi fungsi-fungsi pembantu dan konstanta global.

import json
import os
import platform

# Konstanta yang bisa diakses dari file lain
DATA_FILE = 'airdrop_data.json'
AIRDROP_RSS_FEED = "https://nitter.net/AirdropO_/rss"

def clear_screen():
    """Membersihkan layar terminal."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def load_data():
    """Memuat data dari file JSON. Jika file tidak ada, buat struktur data baru."""
    if not os.path.exists(DATA_FILE):
        return {
            "my_info": {
                "eth_wallet": "Isi dengan alamat wallet ETH/BSC Anda",
                "sol_wallet": "Isi dengan alamat wallet Solana Anda",
                "twitter": "Isi dengan username Twitter Anda (@username)",
                "telegram": "Isi dengan username Telegram Anda (@username)",
                "discord": "Isi dengan username Discord Anda (user#1234)"
            },
            "airdrops": []
        }
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Jika file rusak atau kosong, kembalikan struktur default
        return {"my_info": {}, "airdrops": []}

def save_data(data):
    """Menyimpan data ke file JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

