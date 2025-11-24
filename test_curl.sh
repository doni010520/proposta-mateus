#!/bin/bash

# Exemplo de uso da API com cURL

echo "🚀 Testando Solar Proposal API"
echo ""

# 1. Health check
echo "1️⃣ Health check..."
curl -s http://localhost:3737/health | python3 -m json.tool
echo ""
echo ""

# 2. Gerar proposta
echo "2️⃣ Gerando proposta..."
curl -s -X POST http://localhost:3737/api/generate-proposal \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "Paroquia Santo Antônio de Pádua",
    "consumo": 4560,
    "valor_modulos": 46028.29,
    "valor_mao_obra": 30000.00,
    "tipo_inversor": "02 inversores fotovoltaico 20,00 kW, fabricado pela SOFAR com AFCI"
  }' | python3 -m json.tool

echo ""
echo "✅ Teste completo!"
