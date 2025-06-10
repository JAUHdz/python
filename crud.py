from sqlalchemy.orm import Session
import models, schemas
import requests
from fastapi import HTTPException
from datetime import date

# Profesiones
def generar_siguiente_id(db: Session):
    ultimo = db.query(models.Profesion).order_by(models.Profesion.id.desc()).first()
    return 1 if ultimo is None else ultimo.id + 1

def obtener_estados_validos():
    try:
        response = requests.get("https://status-spring-app.onrender.com/status")
        if response.status_code == 200:
            estados = response.json()
            # Retornamos una lista con los ids válidos
            return [estado['id'] for estado in estados]
    except Exception:
        pass
    return []


def crear_profesion(db: Session, profesion: schemas.ProfesionCreate):
    estados_validos = obtener_estados_validos()
    if profesion.estado_id not in estados_validos:
        raise HTTPException(status_code=400, detail="estado_id inválido, no existe en la API de estados")

    nuevo_id = generar_siguiente_id(db)
    db_prof = models.Profesion(
        id=nuevo_id,
        fecha=date.today(),
        **profesion.dict()
    )
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof


def obtener_profesiones(db: Session):
    return db.query(models.Profesion).all()

def obtener_profesion_por_nombre(db: Session, nombre: str):
    return db.query(models.Profesion).filter(models.Profesion.nombre == nombre).all()

def actualizar_profesion_por_nombre(db: Session, nombre: str, profesion: schemas.ProfesionCreate):
    db_prof = db.query(models.Profesion).filter(models.Profesion.nombre == nombre).first()
    if not db_prof:
        raise HTTPException(status_code=404, detail="Profesión no encontrada")
    profesion_data = profesion.dict()
    profesion_data['fecha'] = date.today() 
    for key, value in profesion_data.items():
        setattr(db_prof, key, value)
    db.commit()
    db.refresh(db_prof)
    return db_prof

def obtener_profesiones_con_estado(db: Session):
    profesiones = db.query(models.Profesion).all()
    
    try:
        response = requests.get("https://status-spring-app.onrender.com/status")
        estados = response.json() if response.status_code == 200 else []
        estados_dict = {estado['id']: estado['nombre'] for estado in estados}
    except:
        estados_dict = {}

    resultado = []
    for p in profesiones:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "fecha": p.fecha,
            "estado_id": p.estado_id,
            "nombre_estado": estados_dict.get(p.estado_id, "Desconocido"),
            # otros campos que tengas en profesion
        })
    return resultado

def obtener_profesion_por_nombre_con_estado(db: Session, nombre: str):
    profesiones = db.query(models.Profesion).filter(models.Profesion.nombre == nombre).all()

    try:
        response = requests.get("https://status-spring-app.onrender.com/status")
        estados = response.json() if response.status_code == 200 else []
        estados_dict = {estado['id']: estado['nombre'] for estado in estados}
    except:
        estados_dict = {}

    resultado = []
    for p in profesiones:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "fecha": p.fecha,
            "estado_id": p.estado_id,
            "nombre_estado": estados_dict.get(p.estado_id, "Desconocido"),
            # puedes agregar más campos aquí si tu modelo los tiene
        })
    return resultado



# ProfesionesUsuario
def persona_existe(persona_id: int) -> bool:
    try:
        response = requests.get("https://microservicioinenew.onrender.com/api/ine/consulta")
        if response.status_code == 200:
            personas = response.json()
            return any(p['persona_id'] == persona_id for p in personas)
    except Exception:
        return False
    return False

def generar_siguiente_id_usuario(db: Session):
    ultimo = db.query(models.ProfesionUsuario).order_by(models.ProfesionUsuario.id.desc()).first()
    return 1 if ultimo is None else ultimo.id + 1

def crear_profesion_usuario(db: Session, relacion: schemas.ProfesionUsuarioCreate):
    if not persona_existe(relacion.persona_id):
        raise HTTPException(status_code=404, detail="persona_id no existe en el microservicio INE")

    nuevo_id = generar_siguiente_id_usuario(db)
    nueva_relacion = models.ProfesionUsuario(
        id=nuevo_id,
        **relacion.dict()
    )
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion

def obtener_profesiones_usuario(db: Session):
    return db.query(models.ProfesionUsuario).all()

def obtener_profesiones_usuario_por_profesion(db: Session, profesion_id: int):
    return db.query(models.ProfesionUsuario).filter(models.ProfesionUsuario.profesion_id == profesion_id).all()

def obtener_detalle_profesiones_usuario(db: Session):
    relaciones = db.query(models.ProfesionUsuario).all()
    profesiones = {p.id: p.nombre for p in db.query(models.Profesion).all()}
    try:
        personas_response = requests.get("https://microservicioinenew.onrender.com/api/ine/consulta")
        personas = personas_response.json() if personas_response.status_code == 200 else []
        personas_dict = {p['persona_id']: p['nombre'] for p in personas}
    except:
        personas_dict = {}

    resultado = []
    for r in relaciones:
        resultado.append({
            "id": r.id,
            "persona_id": r.persona_id,
            "nombre_persona": personas_dict.get(r.persona_id, "Desconocido"),
            "profesion_id": r.profesion_id,
            "nombre_profesion": profesiones.get(r.profesion_id, "Desconocido")
        })
    return resultado
