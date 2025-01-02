from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from typing import Dict, List, Any, Optional

Base = declarative_base()

class CrewMember(Base):
    __tablename__ = 'crew_data'
    
    crew_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    max_monthly_hours = Column(Integer, nullable=False)
    current_work_hours = Column(Integer, default=0)
    is_on_duty = Column(Integer, default=0)  # 0 = False, 1 = True
    duty_status = Column(Integer, default=0)  # 0,1,2,3 durumları için
    
    def to_dict(self):
        return {
            'crew_id': self.crew_id,
            'name': self.name,
            'role': self.role,
            'max_monthly_hours': self.max_monthly_hours,
            'current_work_hours': self.current_work_hours,
            'duty_status': self.duty_status
        }

class CrewCRUD:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
    
    def create_crew_member(self, data: Dict[str, Any]) -> Optional[int]:
        """Yeni mürettebat üyesi oluştur"""
        with Session(self.engine) as session:
            try:
                crew_member = CrewMember(
                    crew_id=data['crew_id'],
                    name=data['name'],
                    role=data['role'],
                    max_monthly_hours=data['max_monthly_hours'],
                    current_work_hours=data.get('current_work_hours', 0),
                    duty_status=data.get('duty_status', 0)
                )
                session.add(crew_member)
                session.commit()
                return crew_member.crew_id
            except IntegrityError:
                session.rollback()
                return None
    
    def get_all_crew(self) -> List[Dict[str, Any]]:
        """Tüm mürettebat listesini getir"""
        with Session(self.engine) as session:
            crew_members = session.query(CrewMember).all()
            return [member.to_dict() for member in crew_members]
    
    def get_crew_by_id(self, crew_id: int) -> Optional[Dict[str, Any]]:
        """ID'ye göre mürettebat üyesi getir"""
        with Session(self.engine) as session:
            crew_member = session.query(CrewMember).filter(CrewMember.crew_id == crew_id).first()
            return crew_member.to_dict() if crew_member else None
    
    def update_crew_member(self, crew_id: int, data: Dict[str, Any]) -> bool:
        """Mürettebat üyesi bilgilerini güncelle"""
        with Session(self.engine) as session:
            try:
                crew_member = session.query(CrewMember).filter(CrewMember.crew_id == crew_id).first()
                if crew_member:
                    for key, value in data.items():
                        if key != 'crew_id':  # ID'nin değiştirilmesine izin verme
                            setattr(crew_member, key, value)
                    session.commit()
                    return True
                return False
            except IntegrityError:
                session.rollback()
                return False
    
    def delete_crew_member(self, crew_id: int) -> bool:
        """Mürettebat üyesini sil"""
        with Session(self.engine) as session:
            crew_member = session.query(CrewMember).filter(CrewMember.crew_id == crew_id).first()
            if crew_member:
                session.delete(crew_member)
                session.commit()
                return True
            return False
    
    # Özel Sorgular
    def get_crew_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Role göre mürettebat üyelerini getir"""
        with Session(self.engine) as session:
            crew_members = session.query(CrewMember).filter(CrewMember.role == role).all()
            return [member.to_dict() for member in crew_members]
    
    def get_crew_by_duty_status(self, status: int) -> List[Dict[str, Any]]:
        """Görev durumuna göre mürettebat üyelerini getir"""
        with Session(self.engine) as session:
            crew_members = session.query(CrewMember).filter(CrewMember.duty_status == status).all()
            return [member.to_dict() for member in crew_members]
    
    def get_available_crew(self, role: str = None) -> List[Dict[str, Any]]:
        """Müsait mürettebat üyelerini getir (duty_status = 0)"""
        with Session(self.engine) as session:
            query = session.query(CrewMember).filter(CrewMember.duty_status == 0)
            if role:
                query = query.filter(CrewMember.role == role)
            crew_members = query.all()
            return [member.to_dict() for member in crew_members]
    
    def update_work_hours(self, crew_id: int, hours: int) -> bool:
        """Çalışma saatlerini güncelle"""
        with Session(self.engine) as session:
            try:
                crew_member = session.query(CrewMember).filter(CrewMember.crew_id == crew_id).first()
                if crew_member:
                    crew_member.current_work_hours = hours
                    session.commit()
                    return True
                return False
            except IntegrityError:
                session.rollback()
                return False

# Kullanım örneği
if __name__ == "__main__":
    db = CrewCRUD("sqlite:///dbs_in_use/crewlist.db")
    
    # Mürettebat üyesi bilgilerini okuma
    crew_member = db.get_crew_by_id(83613)
    print(f"Mürettebat üyesi bilgileri: {crew_member}")
    
    # Role göre arama
    pilots = db.get_crew_by_role("Captain Pilot")
    print(f"Kaptan pilotlar: {pilots[:5]}")
    
    # Görev durumuna göre arama
    available_crew = db.get_crew_by_duty_status(0)
    print(f"Müsait mürettebat: {available_crew[:5]}")
    
    # Müsait pilotları getir
    available_pilots = db.get_available_crew(role="Captain Pilot")
    print(f"Müsait pilotlar: {available_pilots[:5]}")
    
    # Çalışma saatlerini kontrol et
    crew_with_hours = db.get_crew_by_id(83613)
    print(f"Çalışma saatleri: {crew_with_hours['current_work_hours']}")