# 🚀 Solar Proposal API - Deploy Easypanel

## ✅ Projeto Completo

### Estrutura criada:
```
solar-proposal-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # API FastAPI
│   ├── models.py        # Modelos Pydantic
│   ├── calculos.py      # Lógica de cálculos
│   ├── graficos.py      # Geração de gráficos
│   └── pdf_generator.py # Geração de PDF
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── README.md
└── test_api.py
```

## 📋 Pré-requisitos

- GitHub account
- Easypanel configurado na VPS

## 🔧 Deploy no Easypanel

### 1. Push para GitHub

```bash
cd solar-proposal-api
git init
git add .
git commit -m "Initial commit - Solar Proposal API"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/solar-proposal-api.git
git push -u origin main
```

### 2. Configurar no Easypanel

1. Acesse Easypanel
2. Criar novo App
3. Conectar ao repositório GitHub
4. Configurações:
   - **Port:** 3737
   - **Build Command:** docker build
   - **Start Command:** (automático via Dockerfile)

### 3. Variáveis de ambiente (opcional)

Nenhuma necessária no momento.

## 🧪 Testar localmente

```bash
# Com Docker
docker-compose up --build

# Sem Docker
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 3737

# Testar
python test_api.py
```

## 📡 Endpoints

### Health Check
```bash
GET /health
```

### Gerar Proposta
```bash
POST /api/generate-proposal
Content-Type: application/json

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
    "geracao_anual": 61750.0,
    "investimento_total": 76028.29,
    "ano_retorno": 2,
    "economia_25_anos": 2599344.07,
    "geracao_mensal": [...],
    "payback": [...]
  }
}
```

### Download PDF
```bash
GET /outputs/{uuid}_proposta.pdf
```

## 🎯 Exemplo de uso

```python
import requests

response = requests.post(
    "http://localhost:3737/api/generate-proposal",
    json={
        "cliente": "Paroquia Santo Antônio de Pádua",
        "consumo": 4560,
        "valor_modulos": 46028.29,
        "valor_mao_obra": 30000.00,
        "tipo_inversor": "02 inversores SOFAR 20kW"
    }
)

result = response.json()
pdf_url = f"http://localhost:3737{result['pdf_path']}"
print(f"PDF gerado: {pdf_url}")
```

## ⚙️ Parâmetros de Cálculo

- **Tarifa inicial:** R$ 1,1465/kWh
- **Reajuste anual:** 4%
- **Degradação anual:** 0,7%
- **Potência placa:** 620W (0,62 kWp)
- **Dimensionamento:** Consumo ÷ 70 = Qtd placas

## 📊 Geração Mensal (kWh por placa)

| Mês | kWh | Mês | kWh |
|-----|-----|-----|-----|
| Jan | 88  | Jul | 70  |
| Fev | 83  | Ago | 74  |
| Mar | 81  | Set | 77  |
| Abr | 79  | Out | 80  |
| Mai | 74  | Nov | 85  |
| Jun | 72  | Dez | 87  |

**Média:** 82 kWh/placa/mês

## ✨ Features

✅ Cálculo automático de dimensionamento  
✅ Geração de gráficos (PNG)  
✅ Geração de PDF profissional  
✅ Tabela de payback 25 anos  
✅ API REST documentada  
✅ Docker ready  
✅ Pronto para Easypanel  

## 📝 Próximos passos

- [ ] Adicionar logo Level5
- [ ] Criar página web de visualização (/proposal/{id})
- [ ] Implementar cache de propostas
- [ ] Adicionar autenticação (opcional)
- [ ] Personalização de cores/marca

---

**Desenvolvido para CLAWDEO** 🚀
