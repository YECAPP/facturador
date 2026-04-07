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

