# 📚 Documentación de APIs - Apisdom

**IA Profesional. Integración Simple. Resultados Reales.**

Bienvenido a la documentación oficial de las APIs de Apisdom. Aquí encontrarás todo lo necesario para integrar nuestros servicios de inteligencia artificial en tus aplicaciones.

---

## 🎯 Nuestras APIs

| API | Descripción | Modelo IA | Documentación |
|-----|-------------|-----------|---------------|
| 🎭 **Sentiment API** | Detecta emociones en texto (positivo/negativo/neutro) | DistilBERT (SST-2) | [Ver docs](./SENTIMENT_API.md) |
| 🛡️ **Moderation API** | Identifica contenido tóxico e inapropiado | Toxic-BERT (Jigsaw) | [Ver docs](./MODERATION_API.md) |
| 📈 **Prediction API** | Predicciones de series temporales | NeuralProphet | [Ver docs](./PREDICTION_API.md) |

---

## ⚡ Inicio Rápido (5 minutos)

### Paso 1: Obtén tu API Key

1. Regístrate en [apisdom.com](https://apisdom.com)
2. Ve al Dashboard
3. Copia tu token JWT

### Paso 2: Tu Primera Llamada

```bash
curl -X POST "https://api.apisdom.com/api/v1/sentiment/analyze" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"text": "¡Me encanta este servicio!"}'
```

**Respuesta:**
```json
{
  "text": "¡Me encanta este servicio!",
  "sentiment": "positive",
  "score": 0.9721,
  "warning": null,
  "info_message": null
}
```

---

## 🔐 Autenticación

Todas las APIs usan **Bearer Token (JWT)** en el header `Authorization`:

```
Authorization: Bearer tu_token_jwt_aqui
```

### Obtener tu Token

1. Inicia sesión en tu Dashboard
2. Ve a "API Keys"
3. Genera o copia tu token

### Duración del Token

Los tokens JWT tienen validez de **24 horas**. Después deberás renovarlo desde el Dashboard

### Renovación de Tokens

Los tokens JWT expiran cada **30 días**. Recibirás un email de aviso 7 días antes de la expiración.

---

## 📊 Códigos de Estado

| Código | Significado | Acción |
|--------|-------------|--------|
| `200` | ✅ Éxito | Procesar respuesta |
| `400` | ❌ Request inválido | Revisar parámetros enviados |
| `401` | 🔒 No autorizado | Verificar/renovar token |
| `402` | 💳 Sin créditos | Recargar saldo |
| `429` | ⏱️ Rate limit | Esperar y reintentar |
| `500` | 🔥 Error servidor | Reintentar en 30s |

---

## 🌐 SDKs y Ejemplos

### Lenguajes con Ejemplos

Cada documentación de API incluye ejemplos completos en:

- ✅ **Python** (requests)
- ✅ **JavaScript/Node.js** (fetch)
- ✅ **cURL** (terminal)
- ✅ **PHP** (curl)
- ✅ **C#/.NET** (HttpClient)

### Snippets Rápidos

---

## 🏗️ Arquitectura - Cómo Funciona

```
┌──────────┐         ┌──────────────┐         ┌─────────────┐
│ Tu App   │────────▶│  API Gateway │────────▶│ Servicio IA │
│ (Cliente)│   JWT   │  (api-core)  │         │ (ML Model)  │
└──────────┘         └──────────────┘         └─────────────┘
                            │                        │
                            ▼                        ▼
                     ┌──────────────┐         ┌─────────────┐
                     │ 1. Valida JWT│         │ 3. Procesa  │
                     │ 2. Verifica  │         │    con IA   │
                     │    créditos  │         │ 4. Responde │
                     └──────────────┘         └─────────────┘
```

### ¿Dónde ocurre cada cosa?

| Paso | Ubicación | Qué pasa si falla |
|------|-----------|-------------------|
| **1. Validar JWT** | Cada servicio | Error `401 Unauthorized` |
| **2. Verificar créditos** | API Gateway | Error `402 Payment Required` |
| **3. Rate limiting** | Cada servicio | Error `429 Too Many Requests` |
| **4. Procesar con IA** | Servicio específico | Error `500` (raro) |

> **Transparencia**: Los créditos se descuentan DESPUÉS de ejecutar el modelo IA exitosamente. Si el modelo falla, el crédito NO se consume.

### 🔬 Sección de Transparencia Técnica

Cada documentación de API incluye una sección **"Transparencia Técnica"** donde documentamos:

- ✅ **Modelo exacto** utilizado (nombre de HuggingFace)
- ✅ **Parámetros reales** del código fuente
- ✅ **Umbrales y thresholds** (ej: `is_toxic` = score > 0.7)
- ✅ **Diferencias entre planes** (epochs, rate limits)
- ✅ **Flujo real de créditos** (cuándo se verifican y consumen)

Creemos que los desarrolladores merecen saber exactamente cómo funcionan las APIs que usan. Sin cajas negras.

---

## 🚀 Antes de Ir a Producción

### Código de Ejemplo: Cliente Robusto

Este código maneja TODOS los casos de error reales que puede devolver la API:

<details>
<summary><b>Python - Cliente con Retry y Manejo de Errores</b></summary>

```python
import time
import requests
from typing import Any

class ApisdClient:
    """
    Cliente robusto para APIs de Apisdom.
    Maneja: retry, backoff, rate limit, sin créditos.
    """
    
    def __init__(self, token: str, base_url: str = "https://api.apisdom.com"):
        self.token = token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
    
    def _request_with_retry(
        self, 
        method: str, 
        endpoint: str, 
        json_data: dict | None = None,
        max_retries: int = 3
    ) -> dict[str, Any]:
        """
        Request con retry automático y backoff exponencial.
        
        Maneja:
        - 429: Espera según Retry-After o backoff
        - 500/502/503: Retry con backoff
        - 402: NO reintenta (sin créditos)
        - 401: NO reintenta (token inválido)
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, json=json_data, timeout=30)
                
                # Éxito
                if response.status_code == 200:
                    return response.json()
                
                # Sin créditos - NO reintentar
                if response.status_code == 402:
                    raise CreditosInsuficientesError(
                        "Sin créditos. Recarga en: https://apisdom.com/dashboard"
                    )
                
                # Token inválido - NO reintentar
                if response.status_code == 401:
                    raise TokenInvalidoError(
                        "Token inválido o expirado. Renueva en el Dashboard."
                    )
                
                # Rate limit - Esperar y reintentar
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    print(f"Rate limit. Esperando {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                # Error servidor - Retry con backoff
                if response.status_code >= 500:
                    wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                    print(f"Error {response.status_code}. Retry en {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                # Otros errores - No reintentar
                response.raise_for_status()
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"Timeout. Retry en {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise
        
        raise Exception(f"Falló después de {max_retries} intentos")
    
    def analizar_sentimiento(self, texto: str) -> dict:
        """Analiza sentimiento de un texto."""
        return self._request_with_retry(
            "POST", 
            "/api/v1/sentiment/analyze",
            {"text": texto}
        )
    
    def moderar_contenido(self, texto: str) -> dict:
        """Detecta contenido tóxico."""
        return self._request_with_retry(
            "POST",
            "/api/v1/moderation/moderate", 
            {"text": texto}
        )
    
    def predecir_serie(self, dates: list, values: list, periods: int = 7) -> dict:
        """Predice valores futuros de una serie temporal."""
        return self._request_with_retry(
            "POST",
            "/api/v1/prediction/forecast",
            {"dates": dates, "values": values, "periods": periods}
        )


class CreditosInsuficientesError(Exception):
    """Usuario sin créditos - mostrar mensaje en UI"""
    pass


class TokenInvalidoError(Exception):
    """Token expirado o inválido - redirigir a login"""
    pass


# === USO ===
if __name__ == "__main__":
    client = ApisdClient("tu_token_jwt")
    
    try:
        resultado = client.analizar_sentimiento("¡Excelente servicio!")
        print(f"Sentimiento: {resultado['sentiment']} ({resultado['score']:.0%})")
        
    except CreditosInsuficientesError:
        print("⚠️ Recarga créditos en el Dashboard")
        # Mostrar modal/banner en tu UI
        
    except TokenInvalidoError:
        print("🔒 Sesión expirada, redirigiendo a login...")
        # Redirigir a página de login
```
</details>

<details>
<summary><b>JavaScript/TypeScript - Cliente con Retry</b></summary>

```typescript
/**
 * Cliente robusto para APIs de Apisdom.
 * Maneja retry, backoff, rate limit y errores de créditos.
 */
class ApisdClient {
  private token: string;
  private baseUrl: string;

  constructor(token: string, baseUrl = 'https://api.apisdom.com') {
    this.token = token;
    this.baseUrl = baseUrl;
  }

  private async requestWithRetry<T>(
    method: string,
    endpoint: string,
    body?: object,
    maxRetries = 3
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          method,
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
          },
          body: body ? JSON.stringify(body) : undefined,
        });

        // Éxito
        if (response.ok) {
          return response.json();
        }

        // Sin créditos - NO reintentar
        if (response.status === 402) {
          throw new CreditosInsuficientesError(
            'Sin créditos. Recarga en: https://apisdom.com/dashboard'
          );
        }

        // Token inválido - NO reintentar
        if (response.status === 401) {
          throw new TokenInvalidoError('Token inválido o expirado');
        }

        // Rate limit - Esperar y reintentar
        if (response.status === 429) {
          const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
          console.log(`Rate limit. Esperando ${retryAfter}s...`);
          await this.sleep(retryAfter * 1000);
          continue;
        }

        // Error servidor - Retry con backoff
        if (response.status >= 500) {
          const waitTime = Math.pow(2, attempt) * 1000;
          console.log(`Error ${response.status}. Retry en ${waitTime}ms...`);
          await this.sleep(waitTime);
          continue;
        }

        throw new Error(`HTTP ${response.status}`);

      } catch (error) {
        if (error instanceof CreditosInsuficientesError) throw error;
        if (error instanceof TokenInvalidoError) throw error;
        
        if (attempt < maxRetries - 1) {
          const waitTime = Math.pow(2, attempt) * 2000;
          await this.sleep(waitTime);
          continue;
        }
        throw error;
      }
    }

    throw new Error(`Falló después de ${maxRetries} intentos`);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async analizarSentimiento(texto: string) {
    return this.requestWithRetry<SentimentResponse>(
      'POST',
      '/api/v1/sentiment/analyze',
      { text: texto }
    );
  }

  async moderarContenido(texto: string) {
    return this.requestWithRetry<ModerationResponse>(
      'POST',
      '/api/v1/moderation/moderate',
      { text: texto }
    );
  }
}

class CreditosInsuficientesError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CreditosInsuficientesError';
  }
}

class TokenInvalidoError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TokenInvalidoError';
  }
}

// Tipos de respuesta
interface SentimentResponse {
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
  warning: string | null;
}

interface ModerationResponse {
  text: string;
  is_toxic: boolean;
  toxicity_score: number;
  categories: Record<string, number>;
}

// === USO ===
const client = new ApisdClient('tu_token_jwt');

try {
  const resultado = await client.analizarSentimiento('¡Excelente!');
  console.log(`${resultado.sentiment}: ${(resultado.score * 100).toFixed(0)}%`);
} catch (error) {
  if (error instanceof CreditosInsuficientesError) {
    // Mostrar modal de recarga
    showRechargeModal();
  } else if (error instanceof TokenInvalidoError) {
    // Redirigir a login
    window.location.href = '/login';
  }
}
```
</details>

### Checklist Pre-Producción

- [ ] **Implementar retry con backoff** (código arriba)
- [ ] **Manejar 402** → Mostrar mensaje "Recarga créditos"
- [ ] **Manejar 429** → Esperar según `Retry-After`
- [ ] **Manejar 401** → Redirigir a login
- [ ] **Cachear resultados** idénticos (opcional, ahorra créditos)
- [ ] **No exponer token** en código público (GitHub, etc.)

---

## 📊 Rate Limiting

Cada API tiene límites de peticiones por minuto según tu plan:

| Plan | Límite |
|------|--------|
| Free | 10 req/min |
| Starter | 60 req/min |
| Pro | 300 req/min |

Si excedes el límite recibirás error 429 con header `Retry-After`.

---

## ❌ Códigos de Error

| Código | Significado | Acción |
|--------|-------------|--------|
| `200` | Éxito | Todo correcto |
| `400` | Petición inválida | Revisa el formato del JSON |
| `401` | No autenticado | Verifica tu token JWT |
| `402` | Sin créditos | Recarga tu saldo |
| `422` | Datos inválidos | Revisa los campos requeridos |
| `429` | Rate limit | Espera y reintenta |
| `500` | Error interno | Contacta soporte |

### Ejemplo de Error 402 (Sin créditos)

```json
{
  "detail": "Créditos insuficientes. Recarga tu saldo para continuar."
}
```

---

## 🔗 URLs Base

| API | URL Base |
|-----|----------|
| Sentiment | `https://api.apisdom.com/api/v1/sentiment` |
| Moderation | `https://api.apisdom.com/api/v1/moderation` |
| Prediction | `https://api.apisdom.com/api/v1/prediction` |

---

## 🩺 Health Checks

Cada API expone un endpoint de health check (sin autenticación):

| API | Endpoint |
|-----|----------|
| Sentiment | `GET /api/v1/sentiment/health` |
| Moderation | `GET /api/v1/moderation/health` |
| Prediction | `GET /api/v1/prediction/health` |

**Respuesta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "sentiment"
}
```

---

## 📝 Ejemplos Rápidos

<details>
<summary><b>Python - Análisis de Sentimiento</b></summary>

```python
import requests

def analizar_sentimiento(texto, token):
    response = requests.post(
        "https://api.apisdom.com/api/v1/sentiment/analyze",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"text": texto}
    )
    response.raise_for_status()
    return response.json()

# Uso
resultado = analizar_sentimiento("¡Excelente producto!", "tu_token")
print(f"{resultado['sentiment']}: {resultado['score']:.0%}")
# Output: positive: 97%
```
</details>

<details>
<summary><b>JavaScript - Moderar Contenido</b></summary>

```javascript
async function moderar(texto, token) {
  const res = await fetch('https://api.apisdom.com/api/v1/moderation/moderate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: texto })
  });
  
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Uso
const resultado = await moderar('Gracias por tu ayuda', 'tu_token');
console.log(`Tóxico: ${resultado.is_toxic}`);
// Output: Tóxico: false
```
</details>

<details>
<summary><b>cURL - Predecir Serie Temporal</b></summary>

```bash
curl -X POST "https://api.apisdom.com/api/v1/prediction/forecast" \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "dates": ["2024-01-01","2024-01-02","2024-01-03","2024-01-04","2024-01-05",
              "2024-01-06","2024-01-07","2024-01-08","2024-01-09","2024-01-10"],
    "values": [100,105,102,108,115,112,120,118,125,130],
    "periods": 5
  }'
```
</details>

---

## ⚠️ Límites por Request

| API | Campo | Límite |
|-----|-------|--------|
| Sentiment | `text` | 1-5,000 caracteres |
| Moderation | `text` | 1-5,000 caracteres |
| Prediction | `dates` / `values` | 10-5,000 puntos |
| Prediction | `periods` | 1-365 días |

> **Nota:** Los modelos BERT procesan máximo 512 tokens. Textos más largos serán truncados y recibirás un `warning` en la respuesta.

---

## 💡 Buenas Prácticas

### ✅ Recomendado

- Implementar reintentos con backoff exponencial para errores 429/500
- Cachear resultados idénticos para ahorrar créditos
- Validar datos antes de enviarlos a la API
- Manejar el código 402 en tu UI (mostrar mensaje al usuario)
- Revisar el campo `warning` en las respuestas

### ❌ Evitar

- Hacer llamadas en bucles sin rate limiting
- Ignorar `quality_warning` en Prediction API
- Enviar textos mayores a 5,000 caracteres
- Almacenar tokens JWT en código público (GitHub, etc.)

---

## ❓ Preguntas Frecuentes

<details>
<summary><b>¿Qué pasa si me quedo sin créditos?</b></summary>

Recibirás error 402 (`Créditos insuficientes`). Tus datos y configuración permanecen intactos. Recarga créditos para continuar.
</details>

<details>
<summary><b>¿Por qué la primera llamada es lenta?</b></summary>

En el plan gratuito, la primera petición del día puede tardar ~20 segundos (cold start). Una vez activo, las respuestas son < 500ms.
</details>

<details>
<summary><b>¿Puedo usar las APIs en producción?</b></summary>

¡Sí! Nuestras APIs están diseñadas para producción con alta disponibilidad.
</details>

<details>
<summary><b>¿Almacenan el contenido de mis peticiones?</b></summary>

No almacenamos el contenido de tus requests. Solo guardamos métricas de uso para facturación.
</details>

<details>
<summary><b>¿Qué significa el campo "mape" en Prediction API?</b></summary>

MAPE (Mean Absolute Percentage Error) indica el error promedio del modelo. Un MAPE de 0.05 significa 5% de error. Si es > 0.4 (40%), recibirás un `quality_warning`.
</details>

---

## 📄 Documentación Detallada

| Documento | Contenido |
|-----------|-----------|
| [SENTIMENT_API.md](./SENTIMENT_API.md) | Análisis de sentimiento - Guía completa |
| [MODERATION_API.md](./MODERATION_API.md) | Detección de contenido tóxico - Guía completa |
| [PREDICTION_API.md](./PREDICTION_API.md) | Predicciones de series temporales - Guía completa |

---

## 💬 Soporte

| Canal | Para |
|-------|------|
| 📧 soporte@apisdom.com | Dudas técnicas |
| 📚 Esta documentación | Referencia rápida |

---

<div align="center">

**Apisdom** - IA Profesional. Integración Simple. Resultados Reales.

[Dashboard](https://apisdom.com/dashboard) · [Soporte](mailto:soporte@apisdom.com)

</div>

