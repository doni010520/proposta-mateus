from pydantic import BaseModel, Field
from typing import List, Optional


class ProposalInput(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    consumo: float = Field(..., description="Consumo mensal em kWh", gt=0)
    valor_modulos: float = Field(..., description="Valor dos módulos em R$", gt=0)
    valor_mao_obra: float = Field(..., description="Valor da mão de obra em R$", gt=0)
    tipo_inversor: str = Field(..., description="Descrição do inversor")


class GeracaoMensal(BaseModel):
    mes: int
    geracao: float
    nome_mes: str


class PaybackAnual(BaseModel):
    ano: int
    saldo: float
    economia_mensal: float
    economia_anual: float


class Calculos(BaseModel):
    quantidade_placas: int
    potencia_instalada: float
    geracao_mensal: List[GeracaoMensal]
    geracao_anual: float
    investimento_total: float
    payback: List[PaybackAnual]
    ano_retorno: Optional[int]
    economia_25_anos: float


class ProposalOutput(BaseModel):
    pdf_path: str
    web_url: str
    calculos: Calculos
