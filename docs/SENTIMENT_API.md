# 🎭 Sentiment API

**Análisis de Sentimiento con Inteligencia Artificial**

Detecta automáticamente si un texto expresa emociones positivas, negativas o neutras. Perfecto para analizar opiniones de clientes, reseñas de productos o feedback de usuarios.

---

## 📍 Información General

| Propiedad | Valor |
|-----------|-------|
| **URL Base** | `https://api.apisdom.com/api/v1/sentiment` |
| **Método** | `POST` |
| **Autenticación** | Bearer Token (JWT) |
| **Tipo de Crédito** | `text` |
| **Coste por llamada** | 1 crédito |
| **Modelo IA** | DistilBERT (fine-tuned en SST-2) |
| **Límite de tokens** | 512 tokens (textos largos serán truncados) |

---

## 🔐 Autenticación

Todas las peticiones requieren un token JWT en el header `Authorization`:

```
Authorization: Bearer tu_token_jwt_aqui
```

Puedes obtener tu token desde el panel de usuario en [apisdom.com/dashboard](https://apisdom.com/dashboard).

---

## 📥 Endpoint: Analizar Sentimiento

```
POST /api/v1/sentiment/analyze
```

### Request Body

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `text` | string | ✅ Sí | Texto a analizar. Mínimo 1 carácter, máximo 5000. |

### Ejemplo de Request

```json
{
  "text": "Este producto es absolutamente increíble. La calidad supera todas mis expectativas y el envío fue rapidísimo. ¡Muy recomendado!"
}
```

### Response Exitosa (200 OK)

```json
{
  "text": "Este producto es absolutamente increíble. La calidad supera todas mis expectativas y el envío fue rapidísimo. ¡Muy recomendado!",
  "sentiment": "positive",
  "score": 0.9847,
  "warning": null,
  "info_message": null
}
```

### Campos de la Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `text` | string | El texto que fue analizado |
| `sentiment` | string | Sentimiento detectado: `positive`, `negative` o `neutral` |
| `score` | float | Confianza del modelo (0.0 a 1.0). Cuanto más cercano a 1, mayor certeza. |
| `warning` | string \| null | Aviso si el texto fue truncado (textos muy largos) |
| `info_message` | string \| null | Mensaje informativo para usuarios del plan gratuito |

---

## 💻 Ejemplos de Código

### Python

```python
import requests

API_URL = "https://api.apisdom.com/api/v1/sentiment/analyze"
TOKEN = "tu_token_jwt_aqui"

def analizar_sentimiento(texto):
    """
    Analiza el sentimiento de un texto.
    
    Args:
        texto: String con el texto a analizar (máx 5000 caracteres)
    
    Returns:
        dict con sentiment, score y detalles
    """
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={"text": texto}
    )
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 402:
        raise Exception("Sin créditos. Recarga tu saldo en apisdom.com")
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Ejemplo de uso
resultado = analizar_sentimiento("Me encanta este servicio, funciona perfecto!")
print(f"Sentimiento: {resultado['sentiment']}")
print(f"Confianza: {resultado['score']:.2%}")
# Output:
# Sentimiento: positive
# Confianza: 97.32%
```

### JavaScript / Node.js

```javascript
const API_URL = 'https://api.apisdom.com/api/v1/sentiment/analyze';
const TOKEN = 'tu_token_jwt_aqui';

async function analizarSentimiento(texto) {
  /**
   * Analiza el sentimiento de un texto.
   * @param {string} texto - Texto a analizar (máx 5000 caracteres)
   * @returns {Promise<Object>} - Resultado con sentiment, score y detalles
   */
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: texto })
  });

  if (response.status === 402) {
    throw new Error('Sin créditos. Recarga tu saldo en apisdom.com');
  }

  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  return response.json();
}

// Ejemplo de uso
analizarSentimiento('El producto llegó roto y nadie me ayuda')
  .then(resultado => {
    console.log(`Sentimiento: ${resultado.sentiment}`);
    console.log(`Confianza: ${(resultado.score * 100).toFixed(2)}%`);
    // Output:
    // Sentimiento: negative
    // Confianza: 94.56%
  })
  .catch(console.error);
```

### cURL

```bash
curl -X POST "https://api.apisdom.com/api/v1/sentiment/analyze" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -H "Content-Type: application/json" \
  -d '{"text": "La atención al cliente fue excelente, resolvieron mi problema en minutos."}'
```

### PHP

```php
<?php
$api_url = 'https://api.apisdom.com/api/v1/sentiment/analyze';
$token = 'tu_token_jwt_aqui';

function analizarSentimiento($texto) {
    global $api_url, $token;
    
    $ch = curl_init($api_url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $token,
            'Content-Type: application/json'
        ],
        CURLOPT_POSTFIELDS => json_encode(['text' => $texto])
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 402) {
        throw new Exception('Sin créditos. Recarga tu saldo en apisdom.com');
    }
    
    return json_decode($response, true);
}

// Ejemplo de uso
$resultado = analizarSentimiento('El servicio técnico tardó mucho pero al final lo solucionaron');
echo "Sentimiento: " . $resultado['sentiment'] . "\n";
echo "Confianza: " . number_format($resultado['score'] * 100, 2) . "%\n";
// Output:
// Sentimiento: neutral
// Confianza: 62.18%
?>
```

### C# / .NET

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

public class SentimentApiClient
{
    private readonly HttpClient _client;
    private const string API_URL = "https://api.apisdom.com/api/v1/sentiment/analyze";

    public SentimentApiClient(string token)
    {
        _client = new HttpClient();
        _client.DefaultRequestHeaders.Add("Authorization", $"Bearer {token}");
    }

    public async Task<SentimentResult> AnalizarSentimientoAsync(string texto)
    {
        var content = new StringContent(
            JsonSerializer.Serialize(new { text = texto }),
            Encoding.UTF8,
            "application/json"
        );

        var response = await _client.PostAsync(API_URL, content);

        if (response.StatusCode == System.Net.HttpStatusCode.PaymentRequired)
        {
            throw new Exception("Sin créditos. Recarga tu saldo en apisdom.com");
        }

        response.EnsureSuccessStatusCode();
        
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<SentimentResult>(json);
    }
}

public class SentimentResult
{
    public string Text { get; set; }
    public string Sentiment { get; set; }
    public double Score { get; set; }
    public string? Warning { get; set; }
    public string? InfoMessage { get; set; }
}

// Ejemplo de uso
var client = new SentimentApiClient("tu_token_jwt_aqui");
var resultado = await client.AnalizarSentimientoAsync("¡Producto de primera calidad!");
Console.WriteLine($"Sentimiento: {resultado.Sentiment}");
Console.WriteLine($"Confianza: {resultado.Score:P2}");
```

---

## 📊 Casos de Uso Prácticos

### 1. Análisis de Reseñas de Productos

```python
reseñas = [
    "Excelente relación calidad-precio",
    "Llegó tarde y con el embalaje dañado",
    "Hace lo que promete, nada más",
]

for reseña in reseñas:
    resultado = analizar_sentimiento(reseña)
    print(f"'{reseña[:30]}...' → {resultado['sentiment']} ({resultado['score']:.0%})")

# Output:
# 'Excelente relación calidad-pr...' → positive (89%)
# 'Llegó tarde y con el embalaje...' → negative (92%)
# 'Hace lo que promete, nada más...' → neutral (67%)
```

### 2. Clasificación Automática de Tickets de Soporte

```python
def priorizar_ticket(mensaje):
    """Asigna prioridad según el sentimiento del cliente."""
    resultado = analizar_sentimiento(mensaje)
    
    if resultado['sentiment'] == 'negative' and resultado['score'] > 0.8:
        return "🔴 URGENTE - Cliente muy insatisfecho"
    elif resultado['sentiment'] == 'negative':
        return "🟡 ALTA - Cliente insatisfecho"
    else:
        return "🟢 NORMAL"

ticket = "Llevo 3 días esperando respuesta y nadie me ayuda. Es inaceptable."
print(priorizar_ticket(ticket))
# Output: 🔴 URGENTE - Cliente muy insatisfecho
```

### 3. Dashboard de Satisfacción en Tiempo Real

```javascript
async function actualizarDashboard(comentarios) {
  const resultados = await Promise.all(
    comentarios.map(c => analizarSentimiento(c))
  );
  
  const stats = {
    positivos: resultados.filter(r => r.sentiment === 'positive').length,
    negativos: resultados.filter(r => r.sentiment === 'negative').length,
    neutros: resultados.filter(r => r.sentiment === 'neutral').length,
    promedioConfianza: resultados.reduce((a, b) => a + b.score, 0) / resultados.length
  };
  
  console.log('📊 Resumen de Satisfacción:');
  console.log(`   ✅ Positivos: ${stats.positivos}`);
  console.log(`   ❌ Negativos: ${stats.negativos}`);
  console.log(`   ➖ Neutros: ${stats.neutros}`);
  
  return stats;
}
```

---

## ⚠️ Códigos de Error

| Código | Significado | Solución |
|--------|-------------|----------|
| `400` | Texto inválido (vacío o muy largo) | Asegúrate de enviar entre 1 y 5000 caracteres |
| `401` | Token inválido o expirado | Obtén un nuevo token desde el dashboard |
| `402` | Sin créditos disponibles | Recarga tu saldo en apisdom.com |
| `429` | Límite de peticiones excedido | Espera antes de reintentar (ver headers de rate limit) |
| `500` | Error interno del servidor | Reintenta en unos segundos. Si persiste, contacta soporte |

---

## � Transparencia Técnica

> **Política de Apisdom**: Creemos que los desarrolladores merecen saber exactamente cómo funcionan las APIs que usan. Esta sección documenta los detalles técnicos verificados directamente del código fuente.

### Cómo Funciona Internamente

```
Tu texto → Tokenización (DistilBERT) → Inferencia → Normalización → Respuesta
         ↓                           ↓             ↓
         512 tokens máx          CPU-bound      POSITIVE → positive
                                 (threadpool)   NEGATIVE → negative
```

### Detalles Verificados del Código

| Aspecto | Valor Real | Archivo Fuente |
|---------|------------|----------------|
| **Modelo** | `distilbert-base-uncased-finetuned-sst-2-english` | sentiment_service.py |
| **Pipeline** | `sentiment-analysis` de HuggingFace | sentiment_service.py |
| **Truncamiento** | 512 tokens (automático) | sentiment.py línea ~70 |
| **Labels originales** | `POSITIVE`, `NEGATIVE` → normalizados a minúsculas | sentiment_service.py |
| **Ejecución** | `run_in_threadpool` (no bloquea async) | sentiment_service.py |

### Créditos: Flujo Real

```
1. Verificar créditos ANTES de ejecutar modelo (CreditChecker.check_credits)
   ↓ Si no hay créditos → HTTP 402 (modelo NO ejecutado, CPU no consumida)
   
2. Ejecutar inferencia BERT
   
3. Consumir crédito DESPUÉS de éxito (CreditChecker.consume_credit)
   ↓ + Registrar uso en Redis para analytics
```

**Nota honesta**: Si la API retorna 200, el crédito ya fue consumido. No hay forma de "revertirlo" si tu aplicación falla después de recibir la respuesta.

### Epochs por Plan (Sin Variación en Sentiment)

Este modelo usa inferencia directa (no entrena), por lo que **no hay diferencia de calidad entre planes**. La diferencia está en:
- **Cold start**: Free tier tiene ~20 segundos de arranque si el servidor estaba inactivo
- **Rate limit**: Free tier tiene límite de peticiones/minuto más bajo

---

## �📝 Notas Importantes

### Sobre el Modelo DistilBERT

El modelo `distilbert-base-uncased-finetuned-sst-2-english` está entrenado para:
- ✅ Textos en **inglés** (rendimiento óptimo)
- ⚠️ Textos en **español/otros idiomas** (rendimiento reducido, funciona pero con menor precisión)

**Limitaciones conocidas:**
- El modelo fue entrenado en reseñas de películas (dataset SST-2)
- Sarcasmo e ironía pueden ser mal interpretados
- Textos muy técnicos o con jerga específica pueden dar resultados neutros

### Sobre el Truncamiento de Texto

El modelo BERT tiene un límite de 512 tokens (~400 palabras). Si tu texto es más largo:
- Se analizarán los primeros 512 tokens
- Recibirás un `warning` en la respuesta indicando el truncamiento
- El análisis seguirá siendo válido pero parcial

**Recomendación**: Para textos largos, divídelos en párrafos y analiza cada uno por separado.

### Sobre el Tiempo de Respuesta

| Plan | Primera petición del día | Peticiones siguientes |
|------|--------------------------|----------------------|
| Free | ~20 segundos (cold start) | < 500ms |
| Starter | < 500ms | < 500ms |
| Pro | < 500ms | < 500ms |

El "cold start" ocurre porque nuestros servidores escalan a cero cuando no hay actividad. Una vez activo, las respuestas son instantáneas.

---

## 🔗 Recursos Relacionados

- [Moderation API](./MODERATION_API.md) - Detecta contenido tóxico
- [Prediction API](./PREDICTION_API.md) - Predicciones de series temporales

---

## 💬 ¿Necesitas Ayuda?

📧 soporte@apisdom.com
