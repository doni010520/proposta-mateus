"""
Gerador de gráficos para proposta
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo
from typing import List
from app.models import GeracaoMensal, PaybackAnual
import io

# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')


def gerar_grafico_geracao_mensal(geracao_mensal: List[GeracaoMensal]) -> bytes:
    """Gera gráfico de barras da geração mensal"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    meses = [g.nome_mes[:3] for g in geracao_mensal]  # Abrevia nomes
    valores = [g.geracao for g in geracao_mensal]
    
    # Cores Level5 (azul profissional)
    cores = ['#2E7D9A'] * 12
    
    bars = ax.bar(meses, valores, color=cores, edgecolor='white', linewidth=0.5)
    
    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
    ax.set_ylabel('Geração (kWh)', fontsize=12, fontweight='bold')
    ax.set_title('PRODUÇÃO DE ENERGIA', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Salva em bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf.read()


def gerar_grafico_payback(payback: List[PaybackAnual]) -> bytes:
    """Gera gráfico de linha do payback (saldo acumulado)"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    anos = [p.ano for p in payback]
    saldos = [p.saldo for p in payback]
    
    # Linha de saldo
    ax.plot(anos, saldos, color='#2E7D9A', linewidth=2.5, marker='o', 
            markersize=4, label='Saldo Acumulado')
    
    # Linha zero
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
    
    # Área positiva/negativa
    ax.fill_between(anos, saldos, 0, where=[s >= 0 for s in saldos], 
                     color='green', alpha=0.1, label='Lucro')
    ax.fill_between(anos, saldos, 0, where=[s < 0 for s in saldos], 
                     color='red', alpha=0.1, label='Investimento')
    
    ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax.set_ylabel('Saldo Acumulado (R$)', fontsize=12, fontweight='bold')
    ax.set_title('RETORNO DO INVESTIMENTO', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    # Formata eixo Y como moeda
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf.read()
