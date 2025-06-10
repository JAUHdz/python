from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID

# ----------------
# Profesiones
# ----------------
class ProfesionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado_id: UUID  # ahora UUID

class ProfesionCreate(ProfesionBase):
    pass

class Profesion(ProfesionBase):
    id: UUID
    fecha: date

    class Config:
        orm_mode = True

# ----------------
# ProfesionUsuario
# ----------------
class ProfesionUsuarioBase(BaseModel):
    persona_id: int
    profesion_id: int

class ProfesionUsuarioCreate(ProfesionUsuarioBase):
    pass

class ProfesionUsuario(ProfesionUsuarioBase):
    id: int

    class Config:
        orm_mode = True

# ----------------
# Detalle con nombre persona y profesión
# ----------------
class ProfesionUsuarioDetalle(BaseModel):
    id: int
    persona_id: int
    nombre_persona: str
    profesion_id: int
    nombre_profesion: str

    class Config:
        orm_mode = True
