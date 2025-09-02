from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from openpyxl import Workbook
import io

def gerar_holerite_pdf(holerite, colaborador, contrato):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, f"Recibo de Vencimento - {holerite.mes:02d}/{holerite.ano}")

    c.setFont("Helvetica", 12)
    y = height - 1.5 * inch
    c.drawString(inch, y, f"Colaborador: {colaborador.nome}")
    c.drawString(inch, y - 0.25 * inch, f"CPF: {colaborador.cpf}")
    c.drawString(inch, y - 0.5 * inch, f"Cargo: {contrato.cargo}")
    
    y -= 1 * inch
    c.line(inch, y, width - inch, y)
    
    c.setFont("Helvetica-Bold", 12)
    y -= 0.25 * inch
    c.drawString(inch, y, "Descrição")
    c.drawString(width - 3*inch, y, "Valor (R$)")

    y -= 0.1 * inch
    c.line(inch, y, width - inch, y)

    c.setFont("Helvetica", 12)
    y -= 0.25 * inch
    c.drawString(inch, y, "Salário Bruto")
    c.drawString(width - 3*inch, y, f"{holerite.salario_bruto:.2f}")

    c.setFont("Helvetica", 12)
    y -= 0.25 * inch
    c.drawString(inch, y, "Desconto INSS")
    c.drawString(width - 3*inch, y, f"- {holerite.desconto_inss:.2f}")

    c.setFont("Helvetica", 12)
    y -= 0.25 * inch
    c.drawString(inch, y, "Desconto IRRF")
    c.drawString(width - 3*inch, y, f"- {holerite.desconto_irrf:.2f}")

    y -= 0.2 * inch
    c.line(inch, y, width - inch, y)

    c.setFont("Helvetica-Bold", 14)
    y -= 0.35 * inch
    c.drawString(inch, y, "Salário Líquido")
    c.drawString(width - 3*inch, y, f"R$ {holerite.salario_liquido:.2f}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def gerar_folha_excel(holerites):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Folha de Pagamento"

    headers = ["ID Colab.", "Nome", "CPF", "Mês/Ano", "Sal. Bruto", "INSS", "IRRF", "Sal. Líquido"]
    sheet.append(headers)

    for holerite in holerites:
        row = [
            holerite.colaborador.id,
            holerite.colaborador.nome,
            holerite.colaborador.cpf,
            f"{holerite.mes:02d}/{holerite.ano}",
            holerite.salario_bruto,
            holerite.desconto_inss,
            holerite.desconto_irrf,
            holerite.salario_liquido,
        ]
        sheet.append(row)

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer