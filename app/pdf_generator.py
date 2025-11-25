"""
Gerador de PDF de proposta comercial
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from typing import List
import os
from datetime import datetime

from app.models import ProposalInput, Calculos


# Textos fixos extraídos do PDF
TEXTO_QUEM_SOMOS = """Somos uma empresa especializada no segmento de engenharia elétrica, com foco no 
desenvolvimento de projetos elétricos e na instalação de sistemas fotovoltaicos. Desde 2019, 
temos trabalhado para oferecer soluções eficientes e sustentáveis, sempre com alto padrão de 
qualidade. Ao longo de nossa trajetória, já realizamos mais de 700 projetos fotovoltaicos, 
contribuindo para a geração de energia limpa e a redução de custos energéticos de nossos 
clientes. Nosso compromisso é entregar excelência em cada etapa do processo, desde o 
planejamento até a execução, garantindo resultados que superam expectativas."""

TEXTO_FUNCIONAMENTO = """O sistema fotovoltaico é composto principalmente por três componentes: painéis solares, inversor e 
medidor bidirecional. Os painéis captam a energia solar e a convertem em energia elétrica de 
corrente contínua (CC). Em seguida, o inversor transforma essa corrente contínua em corrente 
alternada (CA), que pode ser utilizada pelos equipamentos elétricos. O medidor bidirecional 
desempenha um papel essencial ao monitorar a energia produzida pelo sistema. Ele controla o fluxo 
de energia, permitindo o uso da eletricidade da concessionária quando necessário e acumulando 
créditos para a energia excedente gerada pelo sistema solar. Isso elimina a necessidade de baterias 
para armazenar a energia excedente, tornando o sistema mais econômico e eficiente."""

TEXTO_GARANTIA = """A garantia do sistema fotovoltaico é composta por:

• Módulos Fotovoltaicos: Garantia de desempenho linear de 25 anos e garantia contra defeitos de fabricação de 15 anos, fornecida pelo fabricante.

• Inversor: Garantia de 10 anos contra defeitos de fabricação, conforme especificado pelo fabricante.

• Estrutura de Fixação: Garantia contra corrosão e defeitos de fabricação, de acordo com as especificações do fabricante.

• Serviço de Instalação: Garantia de 1 ano, cobrindo a qualidade e a execução técnica do serviço realizado."""

TEXTO_FORMAS_PAGAMENTO = """Oferecemos diversas formas de pagamento para facilitar a aquisição do seu sistema fotovoltaico. 
Entre as opções disponíveis estão:

• Pagamento à Vista: Desconto especial para pagamentos realizados à vista.

• Financiamento Bancário: Parcerias com instituições financeiras que permitem financiar o sistema 
em até 120 meses, com condições acessíveis e taxas competitivas.

• Pagamento Parcelado: Possibilidade de parcelamento direto no cartão.

Todas as opções são planejadas para proporcionar flexibilidade e viabilizar o investimento em 
energia solar de forma prática e acessível."""

TEXTO_DIFERENCIAL = """Em parceria com a Yelum Seguradora, disponibilizamos uma excelente opção de seguro para os 
equipamentos do seu sistema fotovoltaico, proporcionando proteção completa e total 
tranquilidade. O valor do seguro varia entre 1% e 1,5% do custo total do sistema por ano e 
oferece cobertura para:

• Danos acidentais de origem externa;
• Vendavais e chuvas de granizo;
• Incêndios, quedas de raio e explosões;
• Roubo ou furto.

Essa parceria reforça nosso compromisso em oferecer não apenas soluções de qualidade e eficiência, 
mas também a segurança necessária para o seu investimento em energia solar. Caso tenha interesse, 
realizamos a simulação do valor do seguro no momento do fechamento do projeto fotovoltaico e 
finalizamos o processo diretamente com a seguradora."""


def gerar_pdf(
    input_data: ProposalInput,
    calculos: Calculos,
    grafico_geracao_path: str,
    grafico_payback_path: str,
    output_path: str
) -> str:
    """
    Gera PDF da proposta comercial
    
    Args:
        input_data: Dados de entrada
        calculos: Resultados dos cálculos
        grafico_geracao_path: Caminho do gráfico de geração
        grafico_payback_path: Caminho do gráfico de payback
        output_path: Caminho de saída do PDF
    
    Returns:
        Caminho do PDF gerado
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos customizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E7D9A'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2E7D9A'),
        spaceAfter=12,
        fontName='Helvetica-Bold',
        borderPadding=10,
        backColor=colors.HexColor('#E8F4F8')
    )
    
    texto_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # PÁGINA 1 - CAPA
    story.append(Spacer(1, 80*mm))
    story.append(Paragraph("PROPOSTA COMERCIAL", titulo_style))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(f"<b>CLIENTE:</b><br/>{input_data.cliente.upper()}", 
                          ParagraphStyle('ClienteStyle', parent=texto_style, 
                                       fontSize=14, alignment=TA_CENTER)))
    story.append(PageBreak())
    
    # PÁGINA 2 - QUEM SOMOS
    story.append(Paragraph("QUEM SOMOS?", subtitulo_style))
    story.append(Paragraph(TEXTO_QUEM_SOMOS, texto_style))
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("FUNCIONAMENTO DO SISTEMA FOTOVOLTAICO", subtitulo_style))
    story.append(Paragraph(TEXTO_FUNCIONAMENTO, texto_style))
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("DESCRIÇÃO DOS ITENS:", subtitulo_style))
    story.append(Paragraph(f"• {calculos.quantidade_placas} Módulos Fotovoltaicos 620W Mono Honor Solar - PROCEL", texto_style))
    story.append(Paragraph(f"• {input_data.tipo_inversor}", texto_style))
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("GARANTIA", subtitulo_style))
    story.append(Paragraph(TEXTO_GARANTIA, texto_style))
    story.append(PageBreak())
    
    # PÁGINA 3 - INVESTIMENTO
    story.append(Paragraph("INVESTIMENTO", subtitulo_style))
    
    investimento_data = [
        ['KIT FOTOVOLTAICO', f'R$ {input_data.valor_modulos:,.2f}'],
        ['MÃO DE OBRA, PROJETO E PERIFÉRICOS', f'R$ {input_data.valor_mao_obra:,.2f}'],
        investimento_data = [
        ['KIT FOTOVOLTAICO', f'R$ {input_data.valor_kit:,.2f}'],
    ]
    
    investimento_table = Table(investimento_data, colWidths=[120*mm, 50*mm])
    investimento_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D9A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F4F8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(investimento_table)
    story.append(Spacer(1, 15*mm))
    
    story.append(Paragraph("FORMAS DE PAGAMENTO", subtitulo_style))
    story.append(Paragraph(TEXTO_FORMAS_PAGAMENTO, texto_style))
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("DIFERENCIAL!", subtitulo_style))
    story.append(Paragraph(TEXTO_DIFERENCIAL, texto_style))
    story.append(PageBreak())
    
    # PÁGINA 4 - CUSTO X BENEFÍCIO
    story.append(Paragraph("CUSTO X BENEFÍCIO", subtitulo_style))
    story.append(Paragraph(
        f"O gráfico abaixo ilustra a produção estimada de energia mês a mês, baseada na média anual de {int(calculos.geracao_anual)} kWh. "
        "Essa estimativa considera a variação de irradiância solar ao longo do ano, garantindo uma visão realista do desempenho do sistema em diferentes períodos.",
        texto_style
    ))
    story.append(Spacer(1, 5*mm))
    
    # Adiciona gráfico de geração
    if os.path.exists(grafico_geracao_path):
        story.append(Image(grafico_geracao_path, width=170*mm, height=85*mm))
    
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("RETORNO DO INVESTIMENTO", subtitulo_style))
    
    ano_retorno = calculos.ano_retorno if calculos.ano_retorno else "N/A"
    saldo_ano_retorno = next((p.saldo for p in calculos.payback if p.ano == calculos.ano_retorno), 0) if calculos.ano_retorno else 0
    
    story.append(Paragraph(
        f"Uma das etapas mais importantes para avaliar o custo-benefício do sistema fotovoltaico é o cálculo do retorno sobre o investimento. "
        f"Com base na tarifa atual de energia elétrica de R$ {1.1465}/kWh, considerando um reajuste médio de 4% ao ano, projetamos os seguintes resultados:",
        texto_style
    ))
    story.append(Spacer(1, 3*mm))
    
    story.append(Paragraph(
        f"<b>• Lucro a partir do {ano_retorno}º ano:</b> O sistema começará a gerar um retorno acumulado de R$ {saldo_ano_retorno:,.2f}",
        texto_style
    ))
    story.append(Paragraph(
        f"<b>• Retorno significativo em 25 anos:</b> Economia acumulada de R$ {calculos.economia_25_anos:,.2f}",
        texto_style
    ))
    story.append(Spacer(1, 3*mm))
    
    story.append(Paragraph(
        "Com essas premissas, o investimento no sistema fotovoltaico se mostra altamente vantajoso, "
        "garantindo economia no curto prazo e uma valorização significativa no longo prazo.",
        texto_style
    ))
    
    # Adiciona gráfico de payback
    if os.path.exists(grafico_payback_path):
        story.append(Spacer(1, 5*mm))
        story.append(Image(grafico_payback_path, width=170*mm, height=85*mm))
    
    story.append(PageBreak())
    
    # PÁGINA 5 - TABELA DE PAYBACK
    story.append(Paragraph("TABELA DE RETORNO - 25 ANOS", subtitulo_style))
    
    # Prepara dados da tabela
    tabela_data = [['ANO', 'SALDO', 'ECONOMIA MÉDIA MENSAL', 'ECONOMIA ANUAL']]
    
    for p in calculos.payback:
        tabela_data.append([
            str(p.ano),
            f'R$ {p.saldo:,.2f}',
            f'R$ {p.economia_mensal:,.2f}',
            f'R$ {p.economia_anual:,.2f}'
        ])
    
    payback_table = Table(tabela_data, colWidths=[25*mm, 45*mm, 50*mm, 50*mm])
    payback_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D9A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(payback_table)
    
    # Gera PDF
    doc.build(story)
    
    return output_path
