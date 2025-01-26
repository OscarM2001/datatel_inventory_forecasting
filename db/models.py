from sqlalchemy import Column, Integer, String
from .db_connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)  # Clave primaria
    usuario = Column(String, unique=True, index=True)
    password = Column(String)
    rol = Column(String)
