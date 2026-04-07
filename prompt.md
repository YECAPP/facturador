# Desarrollo de App para facturas

## Especificaciones
## Objetivo
Listar unas facturas que estarán dentro del objeto facturas_db en el app.jsx del sitio 

### Backend 
1. Desarrollado en python con FastApi, pydantic uvicorn 
2. Servidor de Railways para desplegar 
### Frontend
1. React 
2. se desplegará directo en railways junto con el main.py


## Estructura del proyecto
mi-proyecto/
├── main.py
├── requirements.txt
├── Procfile
├── package.json
└── src/
    └── App.jsx

## Instrucciones
1. Se te iran pidiendo los codigos de cada uno de los archivos y tu los iras dando conforme se te van pidiendo 
2. no debes dar todo de golpe, ya que el objetivo es que yo entienda paso a paso lo que se está dando 
3. El codigo del main.py se te dará mas adelante en este prompt
4. Dame los pasos para generar el build del react 
5. considera tambien que el main.py apunta a  static/index.html 

## main.py
`
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
# Monta la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")


def root():
    return FileResponse("static/index.html")

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola, {nombre}!"}

# --- Modelo Pydantic (validación automática) ---
class Factura(BaseModel):
    numero: str
    monto: float
    cliente: str
    iva: Optional[bool] = True

facturas_db = [    {"numero": "F001", "monto": 150.00, "cliente": "Juan Pérez", "iva": True},
    {"numero": "F002", "monto": 320.50, "cliente": "María López", "iva": False},
]

# GET con query param
@app.get("/facturas")
def listar_facturas(limit: int = 10, skip: int = 0):
    return facturas_db[skip : skip + limit]

# POST con body validado
@app.post("/facturas")
def crear_factura(factura: Factura):
    facturas_db.append(factura)
    return {"status": "creada", "factura": factura}

# GET con path param
@app.get("/facturas/{numero}")
def obtener_factura(numero: str):
    for f in facturas_db:
        if f.numero == numero:
            return f
    return {"error": "No encontrada"}

@app.post("/facturas/nueva")
def crear_factura_query(
    numero: str,
    monto: float,
    cliente: str,
    iva: bool = True
):
    nueva = {"numero": numero, "monto": monto, "cliente": cliente, "iva": iva}
    facturas_db.append(nueva)
    return {"status": "creada", "factura": nueva}
`