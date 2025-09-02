from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .models import TipoAfastamento

# --- Colaborador ---
class ColaboradorBase(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str

class ColaboradorCreate(ColaboradorBase):
    pass

class Colaborador(ColaboradorBase):
    id: int
    class Config:
        from_attributes = True

# --- Contrato ---
class ContratoBase(BaseModel):
    cargo: str
    salario_bruto: float
    data_admissao: date
    dependentes: int = 0

class ContratoCreate(ContratoBase):
    colaborador_id: int

class Contrato(ContratoBase):
    id: int
    colaborador_id: int
    class Config:
        from_attributes = True

# --- Folha de Pagamento ---
class GerarHoleriteRequest(BaseModel):
    colaborador_id: int
    mes: int
    ano: int

class Holerite(BaseModel):
    id: int
    colaborador_id: int
    mes: int
    ano: int
    salario_bruto: float
    desconto_inss: float
    desconto_irrf: float
    salario_liquido: float
    class Config:
        from_attributes = True

# --- Afastamentos ---
class AfastamentoBase(BaseModel):
    tipo: TipoAfastamento
    data_inicio: date
    data_fim: date
    motivo: Optional[str] = None

class AfastamentoCreate(AfastamentoBase):
    colaborador_id: int

class Afastamento(AfastamentoBase):
    id: int
    colaborador_id: int
    class Config:
        from_attributes = True

# --- Schema completo ---
class ColaboradorComContrato(Colaborador):
    contrato: Optional[Contrato] = None
    afastamentos: List[Afastamento] = []