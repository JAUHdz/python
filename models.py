import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Profesion(Base):
    __tablename__ = 'profesiones'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))
    fecha = Column(Date)
    estado_id = Column(String(36), nullable=False)  # ahora UUID en string

class ProfesionUsuario(Base):
    __tablename__ = 'profesionesusuario'
    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, nullable=False)
    profesion_id = Column(Integer, ForeignKey("profesiones.id"), nullable=False)
