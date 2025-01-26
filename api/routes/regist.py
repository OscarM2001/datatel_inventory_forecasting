from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.db_connection import get_db_session
from db.models import Usuario

router = APIRouter()

class RegisterRequest(BaseModel):
    usuario: str
    password: str
    rol: str

def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/exists")
def user_exists(usuario: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.usuario == usuario).first()
    return {"exists": user is not None}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.usuario == request.usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    new_user = Usuario(usuario=request.usuario, password=request.password, rol=request.rol)
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado con éxito."}
