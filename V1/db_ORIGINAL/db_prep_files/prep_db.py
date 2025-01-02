import sqlite3

# Veritabanı bağlantısı oluştur
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Flights tablosunu oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS Flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    departure TEXT NOT NULL,
    arrival TEXT NOT NULL,
    duration_hours REAL NOT NULL
)
''')

# SQL dosyasını oku
with open('insert_flights.sql', 'r') as file:
    sql_content = file.read()

# INSERT ifadelerini çalıştır
try:
    cursor.executescript(sql_content)
    conn.commit()
    print("Done")
except sqlite3.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()