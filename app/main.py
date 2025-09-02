# Em app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles   # 1. Importar StaticFiles
from fastapi.responses import FileResponse    # 2. Importar FileResponse
from . import models, routers
from .database import engine

# (Não precisamos mais do middleware CORS com esta abordagem)

# Cria as tabelas na base de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Recursos Humanos (Mini RH)",
    description="Sistema para gerir colaboradores, folha de pagamento e férias.",
    version="1.0.0"
)

# 3. Inclui o router da API primeiro
#    Qualquer rota que comece com /colaboradores, /contratos, etc., será tratada por aqui
app.include_router(routers.router)

# 4. Monta a pasta 'static' para servir ficheiros como CSS, JS, imagens (se tiver)
#    Qualquer ficheiro dentro da pasta 'static' será acessível através do caminho '/static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# 5. Rota "apanha-tudo" para servir o index.html
#    Esta é a parte mais importante. Qualquer rota que não corresponda às da API
#    acima, irá devolver o seu frontend. Isto permite que a sua Single-Page Application funcione.
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse("static/index.html")