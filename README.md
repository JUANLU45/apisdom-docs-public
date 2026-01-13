# 📚 Apisdom - Documentación Oficial de APIs

<div align="center">

![Apisdom](https://img.shields.io/badge/Apisdom-APIs%20de%20IA-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**IA Profesional. Integración Simple. Resultados Reales.**

[🌐 Sitio Web](https://apisdom.com) · [📊 Dashboard](https://apisdom.com/dashboard) · [📧 Soporte](mailto:soporte@apisdom.com)

</div>

---

## 🎯 ¿Qué es Apisdom?

Apisdom ofrece APIs de inteligencia artificial listas para producción. Intégralas en minutos, sin necesidad de entrenar modelos ni gestionar infraestructura ML.

---

## 🚀 Nuestras APIs

| API | Descripción | Modelo IA | Documentación |
|-----|-------------|-----------|---------------|
| 🎭 **Sentiment API** | Detecta emociones en texto (positivo/negativo/neutro) | DistilBERT (SST-2) | [Ver docs](./docs/SENTIMENT_API.md) |
| 🛡️ **Moderation API** | Identifica contenido tóxico e inapropiado | Toxic-BERT (Jigsaw) | [Ver docs](./docs/MODERATION_API.md) |
| 📈 **Prediction API** | Predicciones de series temporales | NeuralProphet | [Ver docs](./docs/PREDICTION_API.md) |

---

## ⚡ Inicio Rápido (5 minutos)

### 1. Obtén tu API Key

```
1. Regístrate en https://apisdom.com
2. Ve al Dashboard
3. Copia tu token JWT
```

### 2. Tu Primera Llamada

```bash
curl -X POST "https://api.apisdom.com/api/v1/sentiment/analyze" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"text": "¡Me encanta este servicio!"}'
```

### 3. Respuesta

```json
{
  "text": "¡Me encanta este servicio!",
  "sentiment": "positive",
  "score": 0.9721
}
```

---

## 💻 Ejemplos de Código

### Python

```python
import requests

def analizar_sentimiento(texto, token):
    response = requests.post(
        "https://api.apisdom.com/api/v1/sentiment/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={"text": texto}
    )
    return response.json()

resultado = analizar_sentimiento("¡Excelente producto!", "tu_token")
print(f"{resultado['sentiment']}: {resultado['score']:.0%}")
# Output: positive: 97%
```

### JavaScript

```javascript
async function analizarSentimiento(texto, token) {
  const res = await fetch('https://api.apisdom.com/api/v1/sentiment/analyze', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: texto })
  });
  return res.json();
}

const resultado = await analizarSentimiento('¡Excelente!', 'tu_token');
console.log(`${resultado.sentiment}: ${(resultado.score * 100).toFixed(0)}%`);
```

---

## 📖 Documentación Completa

| Documento | Contenido |
|-----------|-----------|
| [📚 Guía General](./docs/README.md) | Autenticación, códigos de error, buenas prácticas |
| [🎭 Sentiment API](./docs/SENTIMENT_API.md) | Análisis de sentimiento - Guía completa |
| [🛡️ Moderation API](./docs/MODERATION_API.md) | Detección de toxicidad - Guía completa |
| [📈 Prediction API](./docs/PREDICTION_API.md) | Series temporales - Guía completa |
| [🧪 Tests y Validación](./tests/README.md) | Resultados de pruebas automatizadas |

---

## 📊 Códigos de Estado

| Código | Significado | Acción |
|--------|-------------|--------|
| `200` | ✅ Éxito | Procesar respuesta |
| `400` | ❌ Request inválido | Revisar parámetros |
| `401` | 🔒 No autorizado | Verificar token |
| `402` | 💳 Sin créditos | Recargar saldo |
| `429` | ⏱️ Rate limit | Esperar y reintentar |
| `500` | 🔥 Error servidor | Reintentar en 30s |

---

## 🔐 Autenticación

Todas las APIs usan **Bearer Token (JWT)**:

```
Authorization: Bearer tu_token_jwt_aqui
```

Obtén tu token en [apisdom.com/dashboard](https://apisdom.com/dashboard).

---

## 🩺 Health Checks

Verifica el estado de los servicios (sin autenticación):

```bash
curl https://api.apisdom.com/api/v1/sentiment/health
curl https://api.apisdom.com/api/v1/moderation/health
curl https://api.apisdom.com/api/v1/prediction/health
```

---

## ❓ FAQ

<details>
<summary><b>¿Qué pasa si me quedo sin créditos?</b></summary>
Recibirás error 402. Tus datos permanecen intactos. Recarga para continuar.
</details>

<details>
<summary><b>¿Por qué la primera llamada es lenta?</b></summary>
En el plan gratuito, la primera petición del día puede tardar ~20s (cold start). Después, < 500ms.
</details>

<details>
<summary><b>¿Almacenan mis datos?</b></summary>
No almacenamos el contenido de tus requests. Solo métricas de uso para facturación.
</details>

---

## 📞 Soporte

| Canal | Para |
|-------|------|
| 📧 [soporte@apisdom.com](mailto:soporte@apisdom.com) | Dudas técnicas |
| 📚 Esta documentación | Referencia rápida |
| 🐛 [Issues](https://github.com/apisdom/docs/issues) | Reportar errores en docs |

---

## 🔗 Enlaces Útiles

- 🌐 [Sitio Web](https://apisdom.com)
- 📊 [Dashboard](https://apisdom.com/dashboard)
-  [Contacto](mailto:soporte@apisdom.com)

---

<div align="center">

**Apisdom** - IA Profesional. Integración Simple. Resultados Reales.

Copyright © 2026 Apisdom. Todos los derechos reservados.

</div>
