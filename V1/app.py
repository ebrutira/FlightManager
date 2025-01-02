from flask import Flask, render_template, request, jsonify, redirect, url_for
from main import FlightCrewManager
import os

app = Flask(__name__)

# Başlangıç sayfası
@app.route('/')
def baslangic():
    return render_template('baslangic.html')

# Giriş sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Giriş doğrulama (basit bir örnek)
        if username == 'admin' and password == '123':
            return redirect(url_for('index'))  # Ana sayfaya yönlendir
        else:
            return jsonify({'success': False, 'error': 'Geçersiz giriş, lütfen tekrar deneyin.'}), 400

    return render_template('login.html')

# FlightCrewManager instance'ını oluştur
DB_PATH = r"C:\Users\ebrut.LAPTOP-UIMG1LL4\Desktop\V1\V1\dbs_in_use"
CREW_DB = f"sqlite:///{os.path.join(DB_PATH, 'crewlist.db')}"
AIRPLANES_DB = f"sqlite:///{os.path.join(DB_PATH, 'airplanes.db')}"
manager = FlightCrewManager(CREW_DB, AIRPLANES_DB)

# Ana sayfa
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/assign_crew', methods=['POST'])
def assign_crew():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Geçersiz veri gönderildi.'}), 400

        departure = data.get('departure')
        arrival = data.get('arrival')

        if not departure or not arrival:
            return jsonify({'success': False, 'error': 'Kalkış ve varış noktaları belirtilmelidir.'}), 400

        # Mürettebat ve uçak atama işlemi
        result = manager.assign_crew_for_flight(departure, arrival)

        response = {
            'success': True,
            'data': {
                'flight': f"{departure} -> {arrival}",
                'plane_id': result['plane_id'],
                'fuel_cost': result['fuel_cost'],
                'fuel_consumption': result['fuel_consumption'],
                'distance': result['distance'],
                'flight_hours': result['flight_hours'],
                'departure_time': result['departure_time'],
                'arrival_time': result['arrival_time'],
                'crew': [
                    {
                        'crew_id': crew_id,
                        'name': name,
                        'role': role
                    }
                    for crew_id, role, name in result['assigned_crew']
                ]
            }
        }
        return jsonify(response)

    except ValueError as e:
        # Mesafeden kaynaklı hata durumunu yakala
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except KeyError as e:
        # Eksik veri ile ilgili hatalar
        return jsonify({
            'success': False,
            'error': f'Eksik veri: {e}'
        }), 400
    except Exception as e:
        # Genel hataları yakala
        return jsonify({
            'success': False,
            'error': f"Beklenmeyen bir hata oluştu: {e}"
        }), 500

@app.route('/reset', methods=['POST'])
def reset():
    try:
        manager.reset_status()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
