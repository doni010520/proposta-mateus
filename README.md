# Solar Proposal API

API REST para geração automática de propostas comerciais de energia solar.

## Recursos

- Cálculo automático de dimensionamento (placas, potência, inversor)
- Geração de gráficos (produção mensal, payback 25 anos)
- Geração de PDF profissional
- Cálculo de retorno de investimento com degradação e reajuste

## Instalação

### Docker (Recomendado)

```bash
docker build -t solar-proposal-api .
docker run -p 3737:3737 solar-proposal-api
```

### Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 3737
```

## Uso

### Endpoint: POST /api/generate-proposal

```json
{
  "cliente": "Nome do Cliente",
  "consumo": 4560,
  "valor_modulos": 46028.29,
  "valor_mao_obra": 30000.00,
  "tipo_inversor": "02 inversores SOFAR 20kW com AFCI"
}
```

### Resposta

```json
{
  "pdf_path": "/outputs/uuid_proposta.pdf",
  "web_url": "/proposal/uuid",
  "calculos": {
    "quantidade_placas": 65,
    "potencia_instalada": 40.3,
    "geracao_anual": 5330,
    "investimento_total": 76028.29,
    "ano_retorno": 5,
    "economia_25_anos": 1716069.14
  }
}
```

## Deploy Easypanel

1. Push para GitHub
2. Conectar repositório no Easypanel
3. Configurar porta: 3737
4. Deploy automático

## Parâmetros de Cálculo

- **Tarifa inicial:** R$ 1,1465/kWh
- **Reajuste anual:** 4%
- **Degradação:** 0,7%/ano
- **Potência por placa:** 620W
- **Fator de dimensionamento:** Consumo ÷ 70
