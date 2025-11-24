"""
Script de teste da API
"""
import requests
import json

# Configuração
API_URL = "http://localhost:3737"

# Dados de teste (baseados no PDF original)
test_data = {
    "cliente": "Paroquia Santo Antônio de Pádua",
    "consumo": 4560,
    "valor_modulos": 46028.29,
    "valor_mao_obra": 30000.00,
    "tipo_inversor": "02 inversores fotovoltaico 20,00 kW, fabricado pela SOFAR com AFCI"
}

def test_health():
    """Testa endpoint de health"""
    response = requests.get(f"{API_URL}/health")
    print("=== HEALTH CHECK ===")
    print(json.dumps(response.json(), indent=2))
    print()

def test_generate_proposal():
    """Testa geração de proposta"""
    response = requests.post(
        f"{API_URL}/api/generate-proposal",
        json=test_data
    )
    
    print("=== GERAÇÃO DE PROPOSTA ===")
    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\n✅ Proposta gerada com sucesso!")
        print(f"📄 PDF: {API_URL}{result['pdf_path']}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("🚀 Testando Solar Proposal API\n")
    test_health()
    test_generate_proposal()
