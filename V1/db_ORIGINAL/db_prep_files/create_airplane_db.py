import sqlite3
from typing import List, Tuple

def create_airplane_database(db_path: str) -> None:
    """Airplane veritabanını oluştur ve başlangıç verilerini ekle"""
    
    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabloyu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS airplanes (
        plane_id TEXT PRIMARY KEY,
        plane_name TEXT NOT NULL,
        max_monthly_hours INTEGER NOT NULL,
        airplane_current_work_hours INTEGER DEFAULT 0,
        is_available INTEGER DEFAULT 0
    )
    ''')
    
    # Başlangıç verileri
    airplane_data: List[Tuple] = [
        ('TC-3904', 'Sky Falcon', 300, 0, 0),
        ('TC-3231', 'Cloud Runner', 300, 0, 0),
        ('TC-7203', 'Jetstream', 300, 0, 0),
        ('TC-9193', 'Aero Hawk', 300, 0, 0),
        ('TC-6096', 'Storm Eagle', 300, 0, 0),
        ('TC-4458', 'Nimbus Flyer', 300, 0, 0),
        ('TC-2149', 'Thunderbolt', 300, 0, 0),
        ('TC-3148', 'Solar Wind', 300, 0, 0),
        ('TC-4792', 'Aurora Cruiser', 300, 0, 0),
        ('TC-5136', 'Comet Streak', 300, 0, 0),
        ('TC-6049', 'Stratos Glider', 300, 0, 0),
        ('TC-7285', 'Zephyr Breeze', 300, 0, 0),
        ('TC-8392', 'Sky Liner', 300, 0, 0),
        ('TC-1824', 'Twilight Arrow', 300, 0, 0),
        ('TC-6394', 'Horizon Voyager', 300, 0, 0),
        ('TC-9023', 'Celestial Wing', 300, 0, 0),
        ('TC-6732', 'Cosmic Trail', 300, 0, 0),
        ('TC-5731', 'Stellar Glide', 300, 0, 0),
        ('TC-7814', 'Nebula Swift', 300, 0, 0),
        ('TC-4950', 'Lunar Dart', 300, 0, 0)
    ]
    
    try:
        # Verileri ekle
        cursor.executemany('''
        INSERT INTO airplanes 
        (plane_id, plane_name, max_monthly_hours, airplane_current_work_hours, is_available) 
        VALUES (?, ?, ?, ?, ?)
        ''', airplane_data)
        
        # Değişiklikleri kaydet
        conn.commit()
        print(f"Veritabanı başarıyla oluşturuldu: {db_path}")
        print(f"Toplam {len(airplane_data)} uçak kaydı eklendi")
        
    except sqlite3.Error as e:
        print(f"Hata oluştu: {e}")
        conn.rollback()
    
    finally:
        # Bağlantıyı kapat
        conn.close()

def verify_database(db_path: str) -> None:
    """Veritabanının doğru oluşturulduğunu kontrol et"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Toplam kayıt sayısını kontrol et
        cursor.execute("SELECT COUNT(*) FROM airplanes")
        total_count = cursor.fetchone()[0]
        print(f"\nToplam uçak sayısı: {total_count}")
        
        # Müsait uçak sayısını kontrol et
        cursor.execute("SELECT COUNT(*) FROM airplanes WHERE is_available = 1")
        available_count = cursor.fetchone()[0]
        print(f"Müsait uçak sayısı: {available_count}")
        
        # Örnek kayıtları kontrol et
        cursor.execute("""
        SELECT plane_id, plane_name, airplane_current_work_hours, is_available 
        FROM airplanes 
        LIMIT 5
        """)
        sample_records = cursor.fetchall()
        print("\nÖrnek uçak kayıtları:")
        for record in sample_records:
            print(record)
            
    except sqlite3.Error as e:
        print(f"Kontrol sırasında hata oluştu: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = "airplanes.db"
    
    # Veritabanını oluştur ve verileri ekle
    create_airplane_database(db_path)
    
    # Veritabanını kontrol et
    verify_database(db_path) 