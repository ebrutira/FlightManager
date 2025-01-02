import sqlite3
from typing import List, Tuple

def create_crew_database(db_path: str) -> None:
    """Crew veritabanını oluştur ve başlangıç verilerini ekle"""
    
    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabloyu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crew_data (
        crew_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        max_monthly_hours INTEGER NOT NULL,
        current_work_hours INTEGER DEFAULT 0,
        duty_status INTEGER DEFAULT 0
    )
    """)
    
    # Başlangıç verileri
    initial_data: List[Tuple] = [
        # Captain Pilots
        (37885, 'Linda Taylor', 'Captain Pilot', 90, 0, 0),
        (83613, 'John Brown', 'Captain Pilot', 90, 0, 0),
        (32987, 'Linda Smith', 'Captain Pilot', 90, 0, 0),
        (36841, 'Chris Smith', 'Captain Pilot', 90, 0, 0),
        (43134, 'Robert Jackson', 'Captain Pilot', 90, 0, 0),
        (51234, 'Alice White', 'Captain Pilot', 90, 0, 0),
        (68512, 'Michael Anderson', 'Captain Pilot', 90, 0, 0),
        (79843, 'Sarah Harris', 'Captain Pilot', 90, 0, 0),
        (84532, 'Emily Brown', 'Captain Pilot', 90, 0, 0),

        # Copilots
        (47211, 'Alice White', 'Copilot', 90, 0, 0),
        (58432, 'Sarah Johnson', 'Copilot', 90, 0, 0),
        (69873, 'Robert Taylor', 'Copilot', 90, 0, 0),
        (75684, 'Jane Martin', 'Copilot', 90, 0, 0),
        (81235, 'Chris Thomas', 'Copilot', 90, 0, 0),
        (87321, 'Alex Jackson', 'Copilot', 90, 0, 0),
        (93241, 'John Smith', 'Copilot', 90, 0, 0),
        (97852, 'Emily Taylor', 'Copilot', 90, 0, 0),
        (99312, 'Linda Brown', 'Copilot', 90, 0, 0),

        # Cabin Crew
        (78452, 'Michael Harris', 'Cabin Crew', 90, 0, 0),
        (89231, 'Jane Anderson', 'Cabin Crew', 90, 0, 0),
        (92345, 'Chris Johnson', 'Cabin Crew', 90, 0, 0),
        (81236, 'Robert White', 'Cabin Crew', 90, 0, 0),
        (78123, 'Alice Taylor', 'Cabin Crew', 90, 0, 0),
        (79842, 'Sarah Jackson', 'Cabin Crew', 90, 0, 0),
        (78412, 'Alex Harris', 'Cabin Crew', 90, 0, 0),
        (81523, 'John Anderson', 'Cabin Crew', 90, 0, 0),
        (82345, 'Linda Martin', 'Cabin Crew', 90, 0, 0),
        (89934, 'Emily Brown', 'Cabin Crew', 90, 0, 0),
        (81247, 'Jane White', 'Cabin Crew', 90, 0, 0),
        (78195, 'Chris Taylor', 'Cabin Crew', 90, 0, 0),
        (79231, 'Michael Smith', 'Cabin Crew', 90, 0, 0),
        (80012, 'Alex Johnson', 'Cabin Crew', 90, 0, 0),
        (83451, 'Robert Martin', 'Cabin Crew', 90, 0, 0),
        (89012, 'Sarah Thomas', 'Cabin Crew', 90, 0, 0),
        (82001, 'Linda Jackson', 'Cabin Crew', 90, 0, 0),
        (81423, 'Alice Harris', 'Cabin Crew', 90, 0, 0),
        (87892, 'Chris Anderson', 'Cabin Crew', 90, 0, 0),
        (89451, 'Michael Taylor', 'Cabin Crew', 90, 0, 0),
        (84512, 'Emily Johnson', 'Cabin Crew', 90, 0, 0),
        (85123, 'John Martin', 'Cabin Crew', 90, 0, 0),
        (86431, 'Alice Brown', 'Cabin Crew', 90, 0, 0),
        (87234, 'Chris White', 'Cabin Crew', 90, 0, 0),
        (85145, 'Michael Jackson', 'Cabin Crew', 90, 0, 0),
        (88841, 'Linda Smith', 'Cabin Crew', 90, 0, 0),
        (87521, 'John Johnson', 'Cabin Crew', 90, 0, 0),
        (89034, 'Jane Thomas', 'Cabin Crew', 90, 0, 0),
        (82101, 'Robert Taylor', 'Cabin Crew', 90, 0, 0),
        (85412, 'Emily Harris', 'Cabin Crew', 90, 0, 0),
        (81238, 'Alice White', 'Cabin Crew', 90, 0, 0),
        (83321, 'Sarah Johnson', 'Cabin Crew', 90, 0, 0)
    ]
    
    try:
        # Verileri ekle
        cursor.executemany("""
        INSERT INTO crew_data 
        (crew_id, name, role, max_monthly_hours, current_work_hours, duty_status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, initial_data)
        
        # Değişiklikleri kaydet
        conn.commit()
        print(f"Veritabanı başarıyla oluşturuldu: {db_path}")
        print(f"Toplam {len(initial_data)} personel kaydı eklendi")
        
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
        cursor.execute("SELECT COUNT(*) FROM crew_data")
        total_count = cursor.fetchone()[0]
        print(f"\nToplam kayıt sayısı: {total_count}")
        
        # Role göre personel dağılımını kontrol et
        cursor.execute("""
        SELECT role, COUNT(*) 
        FROM crew_data 
        GROUP BY role
        """)
        role_counts = cursor.fetchall()
        print("\nRole göre personel dağılımı:")
        for role, count in role_counts:
            print(f"{role}: {count}")
        
        # Örnek kayıtları kontrol et
        cursor.execute("""
        SELECT * FROM crew_data 
        LIMIT 5
        """)
        sample_records = cursor.fetchall()
        print("\nÖrnek kayıtlar:")
        for record in sample_records:
            print(record)
            
    except sqlite3.Error as e:
        print(f"Kontrol sırasında hata oluştu: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = "crewlist.db"
    
    # Veritabanını oluştur ve verileri ekle
    create_crew_database(db_path)
    
    # Veritabanını kontrol et
    verify_database(db_path) 