from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class TipoAfastamento(enum.Enum):
    FERIAS = "Férias"
    LICENCA_MEDICA = "Licença Médica"
    LICENCA_MATERNIDADE = "Licença Maternidade"
    OUTRO = "Outro"

class Colaborador(Base):
    __tablename__ = "colaboradores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    
    contrato = relationship("Contrato", back_populates="colaborador", uselist=False, cascade="all, delete-orphan")
    holerites = relationship("Holerite", back_populates="colaborador", cascade="all, delete-orphan")
    afastamentos = relationship("Afastamento", back_populates="colaborador", cascade="all, delete-orphan")

class Contrato(Base):
    __tablename__ = "contratos"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False, unique=True)
    cargo = Column(String, nullable=False)
    salario_bruto = Column(Float, nullable=False)
    data_admissao = Column(Date, nullable=False)
    dependentes = Column(Integer, default=0)

    colaborador = relationship("Colaborador", back_populates="contrato")

class Holerite(Base):
    __tablename__ = "holerites"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    salario_bruto = Column(Float)
    desconto_inss = Column(Float)
    desconto_irrf = Column(Float)
    salario_liquido = Column(Float)
    
    colaborador = relationship("Colaborador", back_populates="holerites")

class Afastamento(Base):
    __tablename__ = "afastamentos"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    tipo = Column(Enum(TipoAfastamento), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    motivo = Column(String, nullable=True)

    colaborador = relationship("Colaborador", back_populates="afastamentos")