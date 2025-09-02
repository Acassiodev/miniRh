from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
from . import schemas, models, payroll_service, report_service
from .database import get_db

router = APIRouter()

# --- Colaboradores ---
@router.post("/colaboradores", response_model=schemas.Colaborador, status_code=status.HTTP_201_CREATED)
def criar_colaborador(colaborador: schemas.ColaboradorCreate, db: Session = Depends(get_db)):
    db_colaborador = models.Colaborador(**colaborador.model_dump())
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    return db_colaborador

@router.get("/colaboradores", response_model=List[schemas.ColaboradorComContrato])
def ler_colaboradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    colaboradores = db.query(models.Colaborador).options(
        joinedload(models.Colaborador.contrato),
        joinedload(models.Colaborador.afastamentos)
    ).offset(skip).limit(limit).all()
    return colaboradores

# --- Contratos ---
@router.post("/contratos", response_model=schemas.Contrato, status_code=status.HTTP_201_CREATED)
def criar_contrato(contrato: schemas.ContratoCreate, db: Session = Depends(get_db)):
    db_contrato = models.Contrato(**contrato.model_dump())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

# --- Folha de Pagamento ---
@router.post("/folha-de-pagamento/gerar", response_model=schemas.Holerite, status_code=status.HTTP_201_CREATED)
def gerar_holerite(request: schemas.GerarHoleriteRequest, db: Session = Depends(get_db)):
    holerite = payroll_service.gerar_holerite_para_colaborador(db, request)
    if not holerite:
        raise HTTPException(status_code=404, detail="Contrato não encontrado para este colaborador")
    return holerite

@router.get("/colaboradores/{colaborador_id}/decimo-terceiro/{ano}")
def calcular_decimo_terceiro(colaborador_id: int, ano: int, db: Session = Depends(get_db)):
    contrato = db.query(models.Contrato).filter(models.Contrato.colaborador_id == colaborador_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    
    calculo = payroll_service.calcular_decimo_terceiro(contrato, ano)
    return calculo

# --- Afastamentos ---
@router.post("/afastamentos", response_model=schemas.Afastamento, status_code=status.HTTP_201_CREATED)
def criar_afastamento(afastamento: schemas.AfastamentoCreate, db: Session = Depends(get_db)):
    db_afastamento = models.Afastamento(**afastamento.model_dump())
    db.add(db_afastamento)
    db.commit()
    db.refresh(db_afastamento)
    return db_afastamento

@router.get("/colaboradores/{colaborador_id}/afastamentos", response_model=List[schemas.Afastamento])
def ler_afastamentos_do_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    afastamentos = db.query(models.Afastamento).filter(models.Afastamento.colaborador_id == colaborador_id).all()
    return afastamentos

# --- Relatórios ---
@router.get("/folha-de-pagamento/{holerite_id}/pdf")
def baixar_holerite_pdf(holerite_id: int, db: Session = Depends(get_db)):
    holerite = db.query(models.Holerite).options(
        joinedload(models.Holerite.colaborador).joinedload(models.Colaborador.contrato)
    ).filter(models.Holerite.id == holerite_id).first()
    if not holerite:
        raise HTTPException(status_code=404, detail="Holerite não encontrado")
    pdf_buffer = report_service.gerar_holerite_pdf(holerite, holerite.colaborador, holerite.colaborador.contrato)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=holerite_{holerite.colaborador.nome.split()[0]}_{holerite.mes}_{holerite.ano}.pdf"
    })

@router.get("/relatorios/folha-de-pagamento")
def baixar_relatorio_excel(mes: int, ano: int, db: Session = Depends(get_db)):
    holerites = db.query(models.Holerite).options(
        joinedload(models.Holerite.colaborador)
    ).filter(models.Holerite.mes == mes, models.Holerite.ano == ano).all()
    if not holerites:
        raise HTTPException(status_code=404, detail="Nenhum holerite encontrado para este período")
    excel_buffer = report_service.gerar_folha_excel(holerites)
    filename = f"folha_de_pagamento_{mes:02d}_{ano}.xlsx"
    return StreamingResponse(excel_buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })