from . import models, schemas
from sqlalchemy.orm import Session
from datetime import date

# Tabelas de cálculo simplificadas
TABELA_INSS = [
    {"limite": 1500.00, "aliquota": 0.075},
    {"limite": 3000.00, "aliquota": 0.09, "deducao": 22.50},
    {"limite": 6000.00, "aliquota": 0.12, "deducao": 112.50},
    {"limite": 8000.00, "aliquota": 0.14, "deducao": 232.50},
]
TETO_INSS = 950.00
TABELA_IRRF = [
    {"limite": 2200.00, "aliquota": 0.0, "deducao": 0.0},
    {"limite": 3000.00, "aliquota": 0.075, "deducao": 165.00},
    {"limite": 4000.00, "aliquota": 0.15, "deducao": 390.00},
    {"limite": 5000.00, "aliquota": 0.225, "deducao": 720.00},
]
DEDUCAO_DEPENDENTE_IRRF = 190.00

def calcular_inss(salario_bruto: float) -> float:
    desconto = 0.0
    for faixa in TABELA_INSS:
        if salario_bruto <= faixa["limite"]:
            desconto = (salario_bruto * faixa["aliquota"]) - faixa.get("deducao", 0)
            break
    if desconto == 0.0:
        desconto = TETO_INSS
    return round(min(desconto, TETO_INSS), 2)

def calcular_irrf(salario_bruto: float, inss: float, dependentes: int) -> float:
    base_calculo = salario_bruto - inss - (dependentes * DEDUCAO_DEPENDENTE_IRRF)
    desconto = 0.0
    for faixa in TABELA_IRRF:
        if base_calculo <= faixa["limite"]:
            desconto = (base_calculo * faixa["aliquota"]) - faixa["deducao"]
            break
    if desconto == 0.0:
        desconto = (base_calculo * 0.275) - 960.00
    return round(max(desconto, 0.0), 2)

def gerar_holerite_para_colaborador(db: Session, request: schemas.GerarHoleriteRequest):
    contrato = db.query(models.Contrato).filter(models.Contrato.colaborador_id == request.colaborador_id).first()
    if not contrato:
        return None
        
    salario_bruto = contrato.salario_bruto
    dependentes = contrato.dependentes
    
    desconto_inss = calcular_inss(salario_bruto)
    desconto_irrf = calcular_irrf(salario_bruto, desconto_inss, dependentes)
    salario_liquido = salario_bruto - desconto_inss - desconto_irrf
    
    novo_holerite = models.Holerite(
        colaborador_id=request.colaborador_id,
        mes=request.mes,
        ano=request.ano,
        salario_bruto=round(salario_bruto, 2),
        desconto_inss=desconto_inss,
        desconto_irrf=desconto_irrf,
        salario_liquido=round(salario_liquido, 2)
    )
    db.add(novo_holerite)
    db.commit()
    db.refresh(novo_holerite)
    
    return novo_holerite

def calcular_decimo_terceiro(contrato: models.Contrato, ano: int):
    meses_trabalhados = 0
    if contrato.data_admissao.year < ano:
        meses_trabalhados = 12
    elif contrato.data_admissao.year == ano:
        meses_trabalhados = (12 - contrato.data_admissao.month) + 1
        if contrato.data_admissao.day > 15:
            meses_trabalhados -= 1
    
    valor_proporcional = (contrato.salario_bruto / 12) * meses_trabalhados
    return {"meses_trabalhados": meses_trabalhados, "valor_bruto_13": round(valor_proporcional, 2)}