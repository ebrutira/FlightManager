from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Airplane(Base):
    __tablename__ = 'airplanes'
    
    plane_id = Column(String(10), primary_key=True)  # TC-XXXX formatında
    plane_name = Column(String(100), nullable=False)
    max_monthly_hours = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'plane_id': self.plane_id,
            'plane_name': self.plane_name,
            'max_monthly_hours': self.max_monthly_hours
        }

class AirplaneCRUD:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
    
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
                        if key != 'plane_id':  # ID'nin değiştirilmesine izin verme
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
    
    # Özel Sorgular
    def get_airplanes_by_name(self, name: str) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            airplanes = session.query(Airplane).filter(
                Airplane.plane_name.like(f"%{name}%")
            ).all()
            return [airplane.to_dict() for airplane in airplanes]
    
    def get_airplanes_by_hours(self, min_hours: int, max_hours: int) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            airplanes = session.query(Airplane).filter(
                Airplane.max_monthly_hours.between(min_hours, max_hours)
            ).all()
            return [airplane.to_dict() for airplane in airplanes]

# Kullanım örneği
if __name__ == "__main__":
    db = AirplaneCRUD("sqlite:///dbs_in_use/airplanes.db")
    
    # Yeni uçak ekleme örneği
    """
    new_airplane = {
        "plane_id": "TC-1234",
        "plane_name": "Test Plane",
        "max_monthly_hours": 300
    }
    plane_id = db.create_airplane(new_airplane)
    print(f"Yeni uçak eklendi. ID: {plane_id}")
    """
    
    # Uçak bilgilerini okuma
    airplane = db.get_airplane_by_id("TC-3904")
    print(f"Uçak bilgileri: {airplane}")
    
    # Uçak güncelleme örneği
    """
    update_data = {
        "plane_name": "Updated Sky Falcon",
        "max_monthly_hours": 320
    }
    success = db.update_airplane("TC-3904", update_data)
    print(f"Güncelleme başarılı: {success}")
    """
    
    # İsme göre arama
    sky_planes = db.get_airplanes_by_name("Sky")
    print(f"'Sky' içeren uçaklar: {sky_planes[:5]}")
    
    # Tüm uçakları getir
    all_airplanes = db.get_all_airplanes()
    print(f"Tüm uçaklar: {all_airplanes[:5]}")
    
    # Belirli saat aralığındaki uçaklar
    hour_range_planes = db.get_airplanes_by_hours(250, 350)
    print(f"250-350 saat arası uçaklar: {hour_range_planes[:5]}")
