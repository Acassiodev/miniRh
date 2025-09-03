# API de Recursos Humanos (Mini RH)

Bem-vindo à API de Mini RH! Este é um sistema FastAPI projetado para gerir as operações essenciais de um departamento de Recursos Humanos, incluindo o registo de colaboradores, a gestão de contratos e o cálculo automatizado da folha de pagamento.

## 🌟 Funcionalidades Principais

- **Gestão de Colaboradores:** Registo completo com informações pessoais e de contacto.
- **Gestão de Contratos:** Detalhes do vínculo laboral, salário, cargo e tipo de contrato.
- **Folha de Pagamento Automatizada:**
    - Geração de recibos de vencimento mensais.
    - **Cálculo automático de Salário Líquido**, com descontos de **INSS** e **IRRF**.
    - Cálculo de **13º Salário** proporcional.
- **Controle de Férias e Afastamentos:** Registe e consulte períodos de ausência.
- **Exportação de Relatórios:**
    - Descarregue um **recibo de vencimento individual em formato PDF**.
    - Exporte um **relatório geral da folha de pagamento em Excel**.
- **Arquitetura Escalável:** Construído com uma arquitetura limpa, pronta para futuras integrações com sistemas contabilísticos.

## 🏁 Como Executar o Projeto

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute a Aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Aceda à documentação interativa** para testar todos os endpoints:
    **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
