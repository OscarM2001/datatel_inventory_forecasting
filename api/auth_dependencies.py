from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.auth_dependencies import decode_access_token

# Punto de entrada para el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Valida el token y extrae el usuario actual."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
