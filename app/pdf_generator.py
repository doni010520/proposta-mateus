"""
API FastAPI para geração de propostas comerciais de energia solar
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from datetime import datetime
from pathlib import Path

from app.models import ProposalInput, ProposalOutput, Calculos
from app.calculos import (
    calcular_potencia_instalada,
    calcular_geracao_mensal,
    calcular_geracao_anual,
    calcular_payback
)
from app.graficos import gerar_grafico_geracao_mensal, gerar_grafico_payback
from app.pdf_generator import gerar_pdf

app = FastAPI(
    title="Solar Proposal API",
    description="API para geração de propostas comerciais de energia solar",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Serve arquivos estáticos
app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "Solar Proposal API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/generate-proposal", response_model=ProposalOutput)
async def generate_proposal(data: ProposalInput):
    """
    Gera proposta comercial completa
    
    Args:
        data: Dados de entrada (cliente, consumo, valores, inversor)
    
    Returns:
        ProposalOutput com caminhos do PDF, URL web e cálculos
    """
    try:
        # 1. Cálculos
        quantidade_placas = data.quantidade_placas
        potencia_instalada = calcular_potencia_instalada(quantidade_placas)
        geracao_mensal = calcular_geracao_mensal(quantidade_placas)
        geracao_anual = calcular_geracao_anual(geracao_mensal)
        investimento_total = data.valor_kit + data.valor_mao_obra
        
        payback_list, ano_retorno, economia_25_anos = calcular_payback(
            geracao_anual, investimento_total
        )
        
        calculos = Calculos(
            quantidade_placas=quantidade_placas,
            potencia_instalada=potencia_instalada,
            geracao_mensal=geracao_mensal,
            geracao_anual=geracao_anual,
            investimento_total=investimento_total,
            payback=payback_list,
            ano_retorno=ano_retorno,
            economia_25_anos=economia_25_anos
        )
        
        # 2. Gerar gráficos
        proposal_id = str(uuid.uuid4())
        
        grafico_geracao_bytes = gerar_grafico_geracao_mensal(geracao_mensal)
        grafico_geracao_path = OUTPUT_DIR / f"{proposal_id}_geracao.png"
        with open(grafico_geracao_path, 'wb') as f:
            f.write(grafico_geracao_bytes)
        
        grafico_payback_bytes = gerar_grafico_payback(payback_list)
        grafico_payback_path = OUTPUT_DIR / f"{proposal_id}_payback.png"
        with open(grafico_payback_path, 'wb') as f:
            f.write(grafico_payback_bytes)
        
        # 3. Gerar PDF
        pdf_filename = f"{proposal_id}_proposta.pdf"
        pdf_path = OUTPUT_DIR / pdf_filename
        
        gerar_pdf(
            input_data=data,
            calculos=calculos,
            grafico_geracao_path=str(grafico_geracao_path),
            grafico_payback_path=str(grafico_payback_path),
            output_path=str(pdf_path)
        )
        
        # 4. Retornar resultado
        return ProposalOutput(
            pdf_path=f"/outputs/{pdf_filename}",
            web_url=f"/proposal/{proposal_id}",
            calculos=calculos
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar proposta: {str(e)}")


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download de arquivo gerado"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/pdf"
    )


@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "outputs_dir": str(OUTPUT_DIR),
        "outputs_writable": os.access(OUTPUT_DIR, os.W_OK)
    }
