from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Airplane(Base):
    __tablename__ = 'airplanes'
    
    plane_id = Column(String(10), primary_key=True)
    plane_name = Column(String(100), nullable=False)
    max_monthly_hours = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'plane_id': self.plane_id,
            'plane_name': self.plane_name,
            'max_monthly_hours': self.max_monthly_hours
        }

class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True)
    departure = Column(String, nullable=False)
    arrival = Column(String, nullable=False)
    duration_hours = Column(Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'departure': self.departure,
            'arrival': self.arrival,
            'duration_hours': self.duration_hours
        }

class FlightSQLAlchemyCRUD:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
    
    # Airplane CRUD Operations
    def create_airplane(self, data: Dict[str, Any]) -> Optional[str]:
        with Session(self.engine) as session:
            try:
                airplane = Airplane(
                    plane_id=data['plane_id'],
                    plane_name=data['plane_name'],
                    max_monthly_hours=data['max_monthly_hours']
                )
                session.add(airplane)
                session.commit()
                return airplane.plane_id
            except IntegrityError:
                session.rollback()
                return None
    
    def get_all_airplanes(self) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            airplanes = session.query(Airplane).all()
            return [airplane.to_dict() for airplane in airplanes]
    
    def get_airplane_by_id(self, plane_id: str) -> Optional[Dict[str, Any]]:
        with Session(self.engine) as session:
            airplane = session.query(Airplane).filter(Airplane.plane_id == plane_id).first()
            return airplane.to_dict() if airplane else None
    
    def update_airplane(self, plane_id: str, data: Dict[str, Any]) -> bool:
        with Session(self.engine) as session:
            try:
                airplane = session.query(Airplane).filter(Airplane.plane_id == plane_id).first()
                if airplane:
                    for key, value in data.items():
                        setattr(airplane, key, value)
                    session.commit()
                    return True
                return False
            except IntegrityError:
                session.rollback()
                return False
    
    def delete_airplane(self, plane_id: str) -> bool:
        with Session(self.engine) as session:
            airplane = session.query(Airplane).filter(Airplane.plane_id == plane_id).first()
            if airplane:
                session.delete(airplane)
                session.commit()
                return True
            return False
    
    # Flight CRUD Operations
    def create_flight(self, data: Dict[str, Any]) -> Optional[int]:
        with Session(self.engine) as session:
            try:
                flight = Flight(
                    departure=data['departure'],
                    arrival=data['arrival'],
                    duration_hours=data['duration_hours']
                )
                session.add(flight)
                session.commit()
                return flight.id
            except IntegrityError:
                session.rollback()
                return None
    
    def get_all_flights(self) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            flights = session.query(Flight).all()
            return [flight.to_dict() for flight in flights]
    
    def get_flight_by_id(self, flight_id: int) -> Optional[Dict[str, Any]]:
        with Session(self.engine) as session:
            flight = session.query(Flight).filter(Flight.id == flight_id).first()
            return flight.to_dict() if flight else None
    
    def update_flight(self, flight_id: int, data: Dict[str, Any]) -> bool:
        with Session(self.engine) as session:
            try:
                flight = session.query(Flight).filter(Flight.id == flight_id).first()
                if flight:
                    for key, value in data.items():
                        setattr(flight, key, value)
                    session.commit()
                    return True
                return False
            except IntegrityError:
                session.rollback()
                return False
    
    def delete_flight(self, flight_id: int) -> bool:
        with Session(self.engine) as session:
            flight = session.query(Flight).filter(Flight.id == flight_id).first()
            if flight:
                session.delete(flight)
                session.commit()
                return True
            return False
    
    # Özel Sorgular
    def get_flights_by_airport(self, airport_code: str) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            flights = session.query(Flight).filter(
                (Flight.departure.like(f"%{airport_code}%")) |
                (Flight.arrival.like(f"%{airport_code}%"))
            ).all()
            return [flight.to_dict() for flight in flights]
    
    def get_flights_by_duration(self, min_hours: float, max_hours: float) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            flights = session.query(Flight).filter(
                Flight.duration_hours.between(min_hours, max_hours)
            ).all()
            return [flight.to_dict() for flight in flights]

# Kullanım örneği
if __name__ == "__main__":
    db = FlightSQLAlchemyCRUD("sqlite:///dbs_in_use/flights.db")
    
    # Uçak ekleme örneği
    """
    new_airplane = {
        "plane_id": "TC-1234",
        "plane_name": "Test Plane",
        "max_monthly_hours": 300
    }
    """
    
    # plane_id = db.create_airplane(new_airplane)
    # print(f"Yeni uçak eklendi. ID: {plane_id}")
    
    # Uçuş ekleme örneği
    new_flight = {
        "departure": "IST (Istanbul)",
        "arrival": "AMS (Amsterdam)",
        "duration_hours": 3.5
    }
    # flight_id = db.create_flight(new_flight)
    # print(f"Yeni uçuş eklendi. ID: {flight_id}")
    
    # Özel sorgu örnekleri
    ist_flights = db.get_flights_by_airport("IST")
    print(f"İstanbul uçuşları: {ist_flights[:5]}\n")
    

    short_flights = db.get_flights_by_duration(1.0, 5.0)
    print(f"1-2 saat arası uçuşlar: {short_flights[:5]}") 