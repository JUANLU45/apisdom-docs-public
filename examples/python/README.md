# Apisdom Python Examples

Ejemplos de uso de las APIs de Apisdom en Python.

## Requisitos

```bash
pip install requests
```

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `quickstart.py` | Ejemplos rápidos de cada API |
| `apisdom_client.py` | Cliente robusto con retry y manejo de errores |

## Uso Rápido

```bash
# 1. Edita el archivo y añade tu token
# 2. Ejecuta
python quickstart.py
```

## Cliente Robusto

El archivo `apisdom_client.py` incluye:

- ✅ Retry automático con backoff exponencial
- ✅ Manejo de rate limit (429)
- ✅ Excepciones específicas para créditos (402) y token inválido (401)
- ✅ Timeout configurable

```python
from apisdom_client import ApisdClient, CreditosInsuficientesError

client = ApisdClient("tu_token")

try:
    resultado = client.analizar_sentimiento("¡Excelente!")
    print(resultado['sentiment'])
except CreditosInsuficientesError:
    print("Recarga créditos en apisdom.com")
```

## Documentación

- [Sentiment API](../../docs/SENTIMENT_API.md)
- [Moderation API](../../docs/MODERATION_API.md)
- [Prediction API](../../docs/PREDICTION_API.md)
