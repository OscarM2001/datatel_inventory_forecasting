
# Activar el entorno virtual
source .venv/Scripts/activate  # En Windows
# source .venv/bin/activate  # En macOS/Linux

echo "Ejecutando FastAPI y Streamlit..."

# Rutas completas a uvicorn y streamlit
.venv/Scripts/uvicorn api.main:app --reload &
.venv/Scripts/streamlit run app/app.py
	