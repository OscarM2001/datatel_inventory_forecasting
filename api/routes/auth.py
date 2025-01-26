from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db_connection import get_db_session
from db.models import Usuario

# Modelo para la solicitud de inicio de sesión
class LoginRequest(BaseModel):
    usuario: str
    password: str

router = APIRouter()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.usuario == credentials.usuario).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"usuario": user.usuario, "rol": user.rol}




