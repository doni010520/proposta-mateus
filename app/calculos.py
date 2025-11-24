"""
Módulo de cálculos para sistema fotovoltaico
"""
from typing import List, Tuple
from app.models import GeracaoMensal, PaybackAnual

# Constantes
GERACAO_POR_PLACA_MES = {
    1: 88,   # Janeiro
    2: 83,   # Fevereiro
    3: 81,   # Março
    4: 79,   # Abril
    5: 74,   # Maio
    6: 72,   # Junho
    7: 70,   # Julho
    8: 74,   # Agosto
    9: 77,   # Setembro
    10: 80,  # Outubro
    11: 85,  # Novembro
    12: 87   # Dezembro
}

NOMES_MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

TARIFA_INICIAL = 1.1465  # R$/kWh
REAJUSTE_ANUAL_TARIFA = 0.04  # 4%
PERDA_EFICIENCIA_ANUAL = 0.007  # 0.7%
POTENCIA_POR_PLACA = 0.62  # kW


def calcular_quantidade_placas(consumo: float) -> int:
    """Calcula quantidade de placas baseado no consumo"""
    return int(consumo / 70)


def calcular_potencia_instalada(quantidade_placas: int) -> float:
    """Calcula potência instalada em kWp"""
    return round(quantidade_placas * POTENCIA_POR_PLACA, 2)


def calcular_geracao_mensal(quantidade_placas: int) -> List[GeracaoMensal]:
    """Calcula geração mensal para cada mês do ano"""
    geracao_mensal = []
    
    for mes in range(1, 13):
        geracao = quantidade_placas * GERACAO_POR_PLACA_MES[mes]
        geracao_mensal.append(GeracaoMensal(
            mes=mes,
            geracao=round(geracao, 2),
            nome_mes=NOMES_MESES[mes]
        ))
    
    return geracao_mensal


def calcular_geracao_anual(geracao_mensal: List[GeracaoMensal]) -> float:
    """Soma geração anual"""
    return sum(g.geracao for g in geracao_mensal)


def calcular_payback(
    geracao_anual: float,
    investimento_total: float,
    anos: int = 25
) -> Tuple[List[PaybackAnual], int, float]:
    """
    Calcula payback considerando:
    - Perda de eficiência de 0.7% ao ano
    - Reajuste de tarifa de 4% ao ano
    
    Returns:
        Tuple com (lista de payback, ano de retorno, economia total em 25 anos)
    """
    payback_list = []
    saldo_acumulado = -investimento_total
    ano_retorno = None
    
    for ano in range(1, anos + 1):
        # Tarifa do ano (com reajuste acumulado)
        tarifa_ano = TARIFA_INICIAL * ((1 + REAJUSTE_ANUAL_TARIFA) ** (ano - 1))
        
        # Geração do ano (com perda de eficiência acumulada)
        geracao_ano = geracao_anual * ((1 - PERDA_EFICIENCIA_ANUAL) ** (ano - 1))
        
        # Economia anual
        economia_anual = geracao_ano * tarifa_ano
        economia_mensal = economia_anual / 12
        
        # Atualiza saldo acumulado
        saldo_acumulado += economia_anual
        
        # Identifica ano de retorno
        if ano_retorno is None and saldo_acumulado > 0:
            ano_retorno = ano
        
        payback_list.append(PaybackAnual(
            ano=ano,
            saldo=round(saldo_acumulado, 2),
            economia_mensal=round(economia_mensal, 2),
            economia_anual=round(economia_anual, 2)
        ))
    
    economia_25_anos = payback_list[-1].saldo if payback_list else 0
    
    return payback_list, ano_retorno, economia_25_anos
