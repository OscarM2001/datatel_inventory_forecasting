# 📊 Proyecto de Tesis: Sistema de Predicción de Inventarios para DATATEL SOLUCIONES S.A.

Este proyecto tiene como objetivo implementar un **sistema de previsión de inventarios en base a las ventas** basado en un modelo predictivo para optimizar la reposición de equipos y mejorar la toma de decisiones en Datatel Soluciones. La solución está diseñada como una aplicación web interactiva utilizando **Streamlit** para la visualización de datos y **ARIMA** como modelo de predicción.

## 📝 Resumen del Proyecto
El sistema aborda los desafíos actuales en la gestión manual del inventario, como la falta de precisión en los niveles de stock y los tiempos prolongados de reposición. A través del modelo ARIMA, se predicen las necesidades de reposición con base en las tendencias históricas de ventas, ayudando a minimizar los costos y a garantizar la disponibilidad de los productos.

El sistema incluye:
- **Dashboard interactivo**: Visualización en tiempo real de los niveles de inventario y predicciones futuras.
- **Matriz de reposición**: Identificación de productos con necesidades críticas de reposición.
- **Predicción de reposición por producto y fecha**: Gráficos detallados para análisis de tendencias.
- **Gestión de usuarios**: Inicio de sesión y registro con roles asignados.

## 🛠️ Tecnologías Utilizadas
- **Python**: Lenguaje principal para el desarrollo.
- **Streamlit**: Herramienta para crear interfaces web interactivas.
- **SQLAlchemy**: Conexión y manipulación de la base de datos.
- **ARIMA**: Modelo predictivo para la optimización del inventario.
- **Plotly**: Creación de gráficos interactivos.

## 🚀 Funcionalidades Principales
### 1. **Inicio de Sesión y Registro de Usuarios**
- Sistema de autenticación que permite gestionar roles de usuario.
- Interfaz intuitiva con opción de registro directo desde la pantalla de inicio de sesión.

### 2. **Dashboard Interactivo**
- Visualización de las métricas clave del modelo ARIMA (MSE, RMSE).
- Representación gráfica de los niveles de inventario y predicciones futuras.

### 3. **Matriz de Reposición de Inventario**
- Análisis de productos según urgencia de reposición, utilizando colores representativos:
  - **Rojo**: Reposición urgente.
  - **Amarillo**: Reposición moderada.
  - **Verde**: Nivel adecuado.
  - **Naranja**: Baja prioridad.

### 4. **Gráficos Interactivos**
- Comparación de ventas históricas vs predicciones.
- Predicción futura por producto y fecha.
- Cantidad recomendada de reposición por producto en gráficos de barras.

# 📊 Proyecto de Tesis: Sistema de Predicción de Inventarios para DATATEL SOLUCIONES S.A.

## 🧑‍🎓 Tema
**Implementación de un modelo predictivo de reposición de inventarios para la optimización de recursos en DATATEL SOLUCIONES S.A.**

Este proyecto tiene como objetivo desarrollar un sistema que utilice modelos predictivos (como ARIMA) para optimizar la reposición de inventarios en una empresa de telecomunicaciones. Incluye una interfaz visual creada con Streamlit para gestionar inventarios y visualizar predicciones.

---

## 🚀 Objetivo del Proyecto
- **Principal:** Optimizar la reposición de inventarios mediante modelos predictivos para mejorar la gestión de recursos y minimizar el riesgo de desabastecimiento.
- **Específicos:**
  - Diseñar un modelo que prediga la reposición de equipos basándose en datos históricos de ventas.
  - Implementar un sistema web interactivo que permita visualizar datos en tiempo real.
  - Automatizar procesos clave, como el seguimiento del inventario y la priorización de productos urgentes.

---

## 📂 Estructura del Proyecto

project/
│
├── app/                 # Lógica principal del sistema
│   ├── app.py           # Control de navegación entre páginas
│   ├── dashboard.py     # Clase para manejar la visualización del dashboard
│   ├── frontend/        # Landing page y elementos visuales
│   
├── Authentication/  # Inicio de sesión y registro de usuarios
├── models/              # Modelos para la predicción de inventarios
├── db/                  # Conexión y consultas a la base de datos
├── Imagen/              # Imágenes utilizadas en la interfaz
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto


## 🛠️ Instalación

### Paso 1: Clonar el Repositorio
Clona este repositorio para obtener el código fuente:

git clone https://github.com/OscarM2001/datatel_inventory_forecasting.git

cd datatel_inventory_forecasting.git

### Paso 2: Crear un Entorno Virtual
Crea un entorno virtual para gestionar las dependencias del proyecto:

python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

### Paso 3: Crear un Entorno Virtual
Instala las dependencias necesarias desde el archivo requirements.txt:
pip install -r requirements.txt

### Paso 4: Paso 4: Configurar la Base de Datos
Configura las credenciales de tu base de datos en el archivo db/db_connection.py.
Asegúrate de que tu base de datos esté funcionando y configurada correctamente.

### Paso 4: Paso 4: Configurar la Base de Datos
Inicia la aplicación con el siguiente comando:

### Paso 5: Ejecutar la Aplicación
Inicia la aplicación con el siguiente comando:
streamlit run app/app.py


## 👥 Autores
Oscar Morán y Xavier Cruz

Universidad de Guayaquil