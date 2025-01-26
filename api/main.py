from fastapi import FastAPI
from api.routes import auth, regist
from fastapi.responses import FileResponse
from api.routes import auth
import os

app = FastAPI(title="Datatel Inventory API", version="1.0.0")

# Registrar rutas
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(regist.router, prefix="/register", tags=["Registration"])

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """
    Devuelve el favicon de la aplicación.
    """
    favicon_path = os.path.join("api", "static", "favicon.ico")
    return FileResponse(favicon_path)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Datatel"}
