from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTAS PROFESIONES
@app.post("/profesiones/", response_model=schemas.Profesion)
def crear_profesion(profesion: schemas.ProfesionCreate, db: Session = Depends(get_db)):
    return crud.crear_profesion(db, profesion)

@app.get("/profesiones/", response_model=List[schemas.Profesion])
def obtener_profesiones(db: Session = Depends(get_db)):
    return crud.obtener_profesiones(db)

@app.get("/profesiones/nombre/{nombre}", response_model=List[schemas.Profesion])
def obtener_profesion_por_nombre(nombre: str, db: Session = Depends(get_db)):
    return crud.obtener_profesion_por_nombre(db, nombre)

@app.put("/profesiones/nombre/{nombre}", response_model=schemas.Profesion)
def actualizar_profesion(nombre: str, profesion: schemas.ProfesionCreate, db: Session = Depends(get_db)):
    return crud.actualizar_profesion_por_nombre(db, nombre, profesion)

@app.get("/profesiones_con_estado")
def leer_profesiones_con_estado(db: Session = Depends(get_db)):
    profesiones = crud.obtener_profesiones_con_estado(db)
    return profesiones

@app.get("/profesiones/nombre-estado/{nombre}")
def obtener_profesion_por_nombre(nombre: str, db: Session = Depends(get_db)):
    return crud.obtener_profesion_por_nombre_con_estado(db, nombre)

# RUTAS PROFESIONES-USUARIO
@app.post("/profesionesusuario/", response_model=schemas.ProfesionUsuario)
def crear_profesion_usuario(data: schemas.ProfesionUsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_profesion_usuario(db, data)

@app.get("/profesionesusuario/", response_model=List[schemas.ProfesionUsuario])
def obtener_profesiones_usuario(db: Session = Depends(get_db)):
    return crud.obtener_profesiones_usuario(db)

@app.get("/profesionesusuario/profesion/{profesion_id}", response_model=List[schemas.ProfesionUsuario])
def obtener_profesiones_usuario_por_profesion(profesion_id: int, db: Session = Depends(get_db)):
    return crud.obtener_profesiones_usuario_por_profesion(db, profesion_id)

@app.get("/profesionesusuario/detalle/", response_model=List[schemas.ProfesionUsuarioDetalle])
def obtener_detalle_profesiones_usuario(db: Session = Depends(get_db)):
    return crud.obtener_detalle_profesiones_usuario(db)
