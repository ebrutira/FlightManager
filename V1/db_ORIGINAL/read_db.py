import sqlite3
from tabulate import tabulate  # Düzenli tablo görünümü için

def show_database_content(db_path):
    try:
        # Veritabanına bağlan
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tüm tabloları bul
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📁 {db_path} veritabanındaki tablolar:\n")
        
        # Her tablo için
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Tablo: {table_name}")
            print("=" * 50)
            
            # Tablo içeriğini al
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Sütun isimlerini al
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Tabulate ile düzenli görüntüle
            print(tabulate(rows, headers=columns, tablefmt='grid'))
            print("\n")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    # Her iki veritabanını kontrol et
    databases = ['flights.db', 'airplanes.db', "crewlist.db"]
    
    for db in databases:
        show_database_content(db)