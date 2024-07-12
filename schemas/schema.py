from pydantic import BaseModel
from typing import List

class AlimentoCreate(BaseModel):
    nome: str
    quantidade: str

class RefeicaoCreate(BaseModel):
    tipo: str
    alimentos: List[AlimentoCreate]

class DietaCreate(BaseModel):
    firebase_uuid: str
    refeicoes: List[RefeicaoCreate]
