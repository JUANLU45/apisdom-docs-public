"""
Ejemplos rápidos de uso de las APIs de Apisdom
Documentación: https://github.com/apisdom/docs
"""

import requests

# Configuración
TOKEN = "tu_token_jwt_aqui"  # Obtén tu token en apisdom.com/dashboard
BASE_URL = "https://api.apisdom.com"


def ejemplo_sentimiento():
    """Analizar sentimiento de un texto"""
    print("\n🎭 SENTIMENT API")
    print("-" * 40)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/sentiment/analyze",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"text": "¡Este producto es increíble! Muy recomendado."}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Texto: {data['text'][:50]}...")
        print(f"Sentimiento: {data['sentiment']}")
        print(f"Confianza: {data['score']:.0%}")
    else:
        print(f"Error: {response.status_code}")


def ejemplo_moderacion():
    """Detectar contenido tóxico"""
    print("\n🛡️ MODERATION API")
    print("-" * 40)
    
    response = requests.post(
        f"{BASE_URL}/api/v1/moderation/moderate",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"text": "Gracias por tu excelente trabajo en este proyecto."}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Texto: {data['text'][:50]}...")
        print(f"¿Tóxico?: {'Sí ❌' if data['is_toxic'] else 'No ✅'}")
        print(f"Score: {data['toxicity_score']:.0%}")
    else:
        print(f"Error: {response.status_code}")


def ejemplo_prediccion():
    """Predecir serie temporal"""
    print("\n📈 PREDICTION API")
    print("-" * 40)
    
    # Datos de ejemplo: 15 días de ventas
    datos = {
        "dates": [f"2024-01-{i:02d}" for i in range(1, 16)],
        "values": [100, 105, 102, 108, 115, 112, 120, 118, 125, 130, 128, 135, 140, 138, 145],
        "periods": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/prediction/forecast",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json=datos
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Error estimado (MAPE): {data['mape']:.1%}")
        print("Predicciones:")
        for p in data['predictions']:
            print(f"  {p['date']}: {p['value']:.2f}")
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    print("=" * 50)
    print("📚 EJEMPLOS DE APISDOM APIs")
    print("=" * 50)
    print(f"\n⚠️ Recuerda cambiar TOKEN por tu token real")
    print(f"   Obtén tu token en: https://apisdom.com/dashboard\n")
    
    ejemplo_sentimiento()
    ejemplo_moderacion()
    ejemplo_prediccion()
    
    print("\n" + "=" * 50)
    print("✅ Ejemplos completados")
    print("📖 Más info: https://github.com/apisdom/docs")
    print("=" * 50)
