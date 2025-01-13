
from sqlalchemy import create_engine, Column, Integer, String, Text, Float,ForeignKey # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import relationship, sessionmaker # type: ignore

#Database connection
engine = create_engine('postgresql://postgres:samina@localhost:5432/leavetypedb', echo = False)
sessionlocal = sessionmaker(bind=engine)
session = sessionlocal()
Base = declarative_base()


#Database tables
#table for leave calculation option
class LeaveCalculationOption(Base):
    __tablename__ = 'leavecalculationoption'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable = False, unique = True)
    formula = Column(Text, nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "formula": self.formula,
        }
    
#table for leave type    
class LeaveType(Base):
    __tablename__ = 'leavetype'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable = False)
    description = Column(String(100))
    calculation_option_id = Column(Integer, ForeignKey('leavecalculationoption.id'))
    calculation_option = relationship('LeaveCalculationOption', backref='leavetypes')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "decsription": self.description,
            "calculation_option" : self.calculation_option.to_dict() if self.calculation_option else None,

        }
   
#table for leave entitlement    
class LeaveEntitlement(Base):
    __tablename__ = 'leaveentitlement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)  # Link to employee table if available
    leave_type_id = Column(Integer, ForeignKey('leavetype.id'), nullable=False)
    entitlement_days = Column(Float, nullable=False)
    used_days = Column(Float, default=0)
    leave_type = relationship('LeaveType', backref='entitlements')

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leave_type_id": self.leave_type_id,
            "entitlement_days": self.entitlement_days,
            "used_days": self.used_days,
            "remaining_days": self.entitlement_days - self.used_days,
        }


#Create tables
    
Base.metadata.create_all(engine)