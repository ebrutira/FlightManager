import requests

API_KEY = "AIzaSyBvnM1wbt1wbPOUOB8tvpmfDCIyoNmKz2Y"

# Google Places API kullanarak havaalanı koordinatlarını al
def get_airport_coordinates(airport_name):
    # Append " airport" to help with correct results and add region=tr (optional).
    search_query = f"{airport_name} airport"
    url = (
        f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
        f"input={search_query}&inputtype=textquery"
        f"&fields=geometry,name&region=tr&key={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result['candidates']:
            return result['candidates'][0]['geometry']['location']
    return None

# Google Distance Matrix API kullanarak mesafe ve süre hesapla
def calculations(origin, destination):
    import math
    lat1, lon1 = map(float, origin.split(","))
    lat2, lon2 = map(float, destination.split(","))

    # radyan cevir
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance_km = 6371 * c  # Earth radius in km

    # Ort. hız 800 km/sa
    flight_speed_kmh = 800.0
    flight_duration_hours = distance_km / flight_speed_kmh
    hours = int(flight_duration_hours)
    minutes = int((flight_duration_hours - hours) * 60)

    distance = f"{distance_km:.2f} km"
    duration = f"{hours} saat {minutes} dakika"

    # Yakıt tüketimi hesaplama (5L/km)
    fuel_consumption = distance_km * 5

    # Yakıt maliyeti hesaplama (1.25$/L)
    fuel_cost = fuel_consumption * 1.25

    return distance, duration, fuel_consumption, fuel_cost


# Kullanım Örneği
if __name__ == "__main__":
    try:
        airport_names = ["Dalaman Havalimanı", "Frankfurt Airport"]
        origin_location = get_airport_coordinates(airport_names[0])
        destination_location = get_airport_coordinates(airport_names[1])
        
        origin = f"{origin_location['lat']},{origin_location['lng']}"
        destination = f"{destination_location['lat']},{destination_location['lng']}"    
        distance, duration, fuel_consumption, fuel_cost = calculations(origin, destination)
        print(f"Mesafe: {distance}")
        print(f"Süre: {duration}")
        print(f"Yakıt Tüketimi: {fuel_consumption:.2f} L")
        print(f"Yakıt Maliyeti: ${fuel_cost:.2f}")

    except Exception as e:
        print(f"Hata: {e}")