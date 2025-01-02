import sqlite3
import re

def create_crew_database():
    # Veritabanı bağlantısı oluştur
    conn = sqlite3.connect('crewlist.db')
    cursor = conn.cursor()

    # Crew_Data tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Crew_Data (
        crew_id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        max_monthly_hours INTEGER,
        current_work_hours INTEGER,
        duty_status INTEGER
    )
    ''')

    # SQL dosyasını oku ve verileri çıkar
    with open('crewlist.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        
        # INSERT INTO satırlarını bul
        insert_pattern = r'\((\d+),\s*\'([^\']+)\',\s*\'([^\']+)\',\s*(\d+),\s*(\d+),\s*(\d+)\)'
        matches = re.findall(insert_pattern, content)

        # Verileri tabloya ekle
        for match in matches:
            crew_id = int(match[0])
            name = match[1]
            role = match[2]
            max_hours = int(match[3])
            current_hours = int(match[4])
            duty_status = int(match[5])

            cursor.execute('''
            INSERT OR REPLACE INTO Crew_Data (crew_id, name, role, max_monthly_hours, current_work_hours, duty_status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (crew_id, name, role, max_hours, current_hours, duty_status))

    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()

# Veritabanını oluştur
create_crew_database()

# Verileri kontrol et
def check_database():
    conn = sqlite3.connect('crewlist.db')
    cursor = conn.cursor()
    
    print("Veritabanındaki kayıtlar:")
    cursor.execute("SELECT * FROM Crew_Data")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}, İsim: {row[1]}, Rol: {row[2]}, Max Saat: {row[3]}, Şu anki saat: {row[4]}, Durum: {row[5]}")
    
    print(f"\nToplam kayıt sayısı: {len(rows)}")
    conn.close()

check_database()