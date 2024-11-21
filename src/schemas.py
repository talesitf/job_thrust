from pydantic import BaseModel

class Vaga(BaseModel):
    descricao: str
    responsabilidades: str
    requisitos: str
    beneficios: str