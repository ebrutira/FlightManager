from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Tuple, Dict
import logging
import os
from google_api_test import calculations, get_airport_coordinates
import math
import random
from datetime import datetime, timedelta

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlightCrewManager:
    def __init__(self, crew_db: str, airplanes_db: str):
        """
        FlightCrewManager sınıfını başlatır.
        
        Args:
            crew_db: Mürettebat veritabanı bağlantı string'i
            airplanes_db: Uçaklar veritabanı bağlantı string'i
        """
        # Crew veritabanı bağlantısı
        self.crew_engine = create_engine(crew_db)
        CrewSession = sessionmaker(bind=self.crew_engine)
        self.crew_session = CrewSession()
        
        # Airplanes veritabanı bağlantısı
        self.airplanes_engine = create_engine(airplanes_db)
        AirplanesSession = sessionmaker(bind=self.airplanes_engine)
        self.airplanes_session = AirplanesSession()
        
    def find_available_crew(self, role: str, flight_hours: float) -> Tuple[int, str]:
        """Crew DB'den uygun mürettebat üyesini bulur."""
        query = text("""
            SELECT crew_id, name 
            FROM Crew_Data 
            WHERE role = :role 
            AND (current_work_hours + :flight_hours) <= max_monthly_hours
            AND duty_status = 0
            ORDER BY current_work_hours ASC
            LIMIT 1
        """)
        
        result = self.crew_session.execute(query, {"role": role, "flight_hours": flight_hours})
        row = result.fetchone()
        
        if row is None:
            raise ValueError(f"Uygun {role} bulunamadı")
            
        crew_id, name = row
        return crew_id, name
        
    def update_crew_hours(self, crew_id: int, flight_hours: float) -> None:
        """Crew DB'de mürettebat üyesinin çalışma saatlerini günceller."""
        query = text("""
            UPDATE Crew_Data 
            SET current_work_hours = current_work_hours + :flight_hours,
                duty_status = 1
            WHERE crew_id = :crew_id
        """)
        
        self.crew_session.execute(query, {"crew_id": crew_id, "flight_hours": flight_hours})
        self.crew_session.commit()
        
    def find_available_airplane(self, flight_hours: float) -> str:
        """Airplanes DB'den uygun uçağı bulur."""
        query = text("""
            SELECT plane_id 
            FROM Airplanes 
            WHERE (airplane_current_work_hours + :flight_hours) <= max_monthly_hours
            AND is_available = 1
            ORDER BY airplane_current_work_hours ASC
            LIMIT 1
        """)
        
        result = self.airplanes_session.execute(query, {"flight_hours": flight_hours})
        plane_id = result.scalar()
        
        if plane_id is None:
            raise ValueError("Uygun uçak bulunamadı")
            
        return plane_id
            
    def update_airplane_hours(self, plane_id: str, flight_hours: float) -> None:
        """Airplanes DB'de uçağın çalışma saatlerini günceller."""
        query = text("""
            UPDATE Airplanes 
            SET airplane_current_work_hours = airplane_current_work_hours + :flight_hours
            WHERE plane_id = :plane_id
        """)
        
        self.airplanes_session.execute(query, {"plane_id": plane_id, "flight_hours": flight_hours})
        self.airplanes_session.commit()
    
    def assign_crew_for_flight(self, departure: str, arrival: str) -> Dict:
        """Uçuş için mürettebat ve uçak ataması yapar."""
        origin_coords = get_airport_coordinates(departure)
        if not origin_coords or "lat" not in origin_coords or "lng" not in origin_coords:
            raise ValueError(f"Could not find coordinates for {departure}")
        origin_lat, origin_lng = origin_coords["lat"], origin_coords["lng"]

        destination_coords = get_airport_coordinates(arrival)
        if not destination_coords or "lat" not in destination_coords or "lng" not in destination_coords:
            raise ValueError(f"Could not find coordinates for {arrival}")
        destination_lat, destination_lng = destination_coords["lat"], destination_coords["lng"]
        
        origin = f"{origin_lat},{origin_lng}"
        destination = f"{destination_lat},{destination_lng}"
        
        distance, duration, fuel_consumption, fuel_cost = calculations(origin, destination)

        if not distance or not duration:
            raise ValueError("Mesafe 300 km'nin altında olduğundan hesaplama yapılamaz..")

        if float(distance.split()[0]) < 300:
            raise ValueError("Mesafe 300 km'nin altında olduğundan hesaplama yapılamaz.")

        # Rastgele uçuş tarihi ve saat hesaplama
        today = datetime.today()
        flight_date = today + timedelta(days=random.randint(60, 180))
        departure_hour = random.randint(0, 23)
        departure_minute = random.randint(0, 59)
        departure_time = datetime.combine(flight_date, datetime.min.time()) + timedelta(hours=departure_hour, minutes=departure_minute)
        arrival_time = departure_time + timedelta(hours=math.ceil(float(duration.split()[0])))

        # flight_hours hesaplama
        try:
            hours = int(duration.split()[0])
            minutes = int(duration.split()[2])
            flight_hours = math.ceil(hours + minutes / 60.0)
        except (ValueError, IndexError):
            raise ValueError(f"Uçuş süresi yanlış formatta: {duration}")

        distance_value = float(distance.split()[0])

        # Uçak ataması
        plane_id = self.find_available_airplane(flight_hours)
        self.update_airplane_hours(plane_id, flight_hours)
        
        # Mürettebat ataması
        required_roles = ['Captain Pilot', 'Copilot', 'Cabin Crew', 'Cabin Crew', 'Cabin Crew']
        assigned_crew = []
        
        for role in required_roles:
            crew_id, name = self.find_available_crew(role, flight_hours)
            self.update_crew_hours(crew_id, flight_hours)
            assigned_crew.append((crew_id, role, name))

        return {
            "assigned_crew": assigned_crew,
            "plane_id": plane_id,
            "fuel_cost": round(fuel_cost, 2),
            "fuel_consumption": round(fuel_consumption, 2),
            "distance": round(distance_value, 2),
            "flight_hours": flight_hours,
            "departure_time": departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            "arrival_time": arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def reset_status(self) -> None:
        """Tüm veritabanlarındaki durumları sıfırlar."""
        try:
            # Crew DB reset
            self.crew_session.execute(text("UPDATE Crew_Data SET duty_status = 0, current_work_hours = 0"))
            self.crew_session.commit()
            
            # Airplanes DB reset
            self.airplanes_session.execute(text("UPDATE Airplanes SET is_available = 1, airplane_current_work_hours = 0"))
            self.airplanes_session.commit()
            
        except Exception as e:
            self.crew_session.rollback()
            self.airplanes_session.rollback()
            logger.error(f"Reset işlemi sırasında hata: {str(e)}")
            raise

    def __del__(self):
        """Tüm session'ları kapatır."""
        self.crew_session.close()
        self.airplanes_session.close()
