# 🛡️ Moderation API

**Detección de Contenido Tóxico con Inteligencia Artificial**

Identifica automáticamente contenido ofensivo, insultos, amenazas, discurso de odio y otros tipos de toxicidad en texto. Esencial para moderar comentarios, chats y contenido generado por usuarios.

---

## 📍 Información General

| Propiedad | Valor |
|-----------|-------|
| **URL Base** | `https://apisdom.com/api/v1` |
| **Método** | `POST` |
| **Autenticación** | API Key (Header `X-API-Key`) |
| **Tipo de Crédito** | `text` |
| **Coste por llamada** | 1 crédito |
| **Modelo IA** | Toxic-BERT (fine-tuned en Jigsaw dataset) |
| **Categorías detectadas** | Múltiples (según modelo toxic-bert) |

### ⏱️ Rate Limits

| Plan | Límite | Cuota Mensual | Precio |
|------|--------|---------------|--------|
| **Prueba Gratuita** | 10 req/min | 1,000 créditos (único uso) | €0 |
| **Plan Starter** | 60 req/min | 10,000 créditos/mes | €4.99/mes |
| **Plan Pro** | 300 req/min | 100,000 créditos/mes | €19.99/mes |

> **Nota sobre cuotas:**
> - **Plan Gratuito**: Los 1,000 créditos son de uso único y NO se resetean.
> - **Planes de pago**: Las cuotas se resetean el día 1 de cada mes a las 00:00 UTC.
> - Si excedes el rate limit, recibirás error `429 Too Many Requests` con header `Retry-After`.

### 📊 Headers Informativos

La API devuelve headers que te permiten controlar tu consumo:

| Header | Descripción |
|--------|-------------|
| `X-RateLimit-Limit` | Tu límite de peticiones por minuto |
| `X-RateLimit-Remaining` | Peticiones restantes en la ventana actual |
| `Retry-After` | Segundos a esperar si recibes 429 |

---

## 🔐 Autenticación

Todas las peticiones requieren tu API Key en el header `X-API-Key`:

```
X-API-Key: tu_api_key_aqui
```

Puedes obtener tu API Key desde el panel de usuario en [apisdom.com/dashboard](https://apisdom.com/dashboard).

---

## 📥 Endpoint: Moderar Contenido

```
POST https://apisdom.com/api/v1/moderacion
```

### Request Body

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `text` | string | ✅ Sí | Texto a moderar. Mínimo 1 carácter, máximo 5000. |

### Ejemplo de Request

```json
{
  "text": "Eres un completo idiota y deberías desaparecer."
}
```

### Response Exitosa (200 OK)

```json
{
  "text": "Eres un completo idiota y deberías desaparecer.",
  "is_toxic": true,
  "toxicity_score": 0.923,
  "categories": {
    "toxic": 0.923,
    "insult": 0.876
  },
  "warning": null,
  "info_message": null
}
```

> **Nota:** El campo `categories` contiene SOLO las etiquetas que el modelo detecta con confianza significativa. Las claves exactas dependen del modelo `unitary/toxic-bert` y pueden variar.

### Campos de la Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `text` | string | El texto que fue analizado |
| `is_toxic` | boolean | `true` si toxicity_score > 0.7, `false` en caso contrario |
| `toxicity_score` | float | Puntuación máxima de toxicidad detectada (0.0 a 1.0) |
| `categories` | object | Desglose por categorías detectadas por el modelo (ver nota abajo) |
| `warning` | string \| null | Aviso si el texto fue truncado (más de 512 tokens) |
| `info_message` | string \| null | Mensaje informativo para usuarios del plan gratuito |

### Sobre las Categorías de Toxicidad

> **Nota técnica:** Las categorías devueltas dependen del modelo `unitary/toxic-bert`. El modelo retorna las etiquetas detectadas con su puntuación de confianza. Las categorías más comunes incluyen:

| Categoría | Descripción |
|-----------|-------------|
| `toxic` | Contenido tóxico general |
| `severe_toxic` | Toxicidad severa/extrema |
| `obscene` | Lenguaje obsceno o vulgar |
| `threat` | Amenazas o intimidación |
| `insult` | Insultos directos |
| `identity_hate` | Discurso de odio por identidad |

**Importante:** La estructura exacta del campo `categories` puede variar según la versión del modelo. Siempre itera sobre las claves devueltas en lugar de asumir nombres específicos.

---

## 💻 Ejemplos de Código

### Python

```python
import requests
from typing import Optional

API_URL = "https://apisdom.com/api/v1/moderacion"
API_KEY = "tu_api_key_aqui"

def moderar_contenido(texto: str) -> dict:
    """
    Analiza un texto para detectar contenido tóxico.
    
    Args:
        texto: String a moderar (máx 5000 caracteres)
    
    Returns:
        dict con is_toxic, toxicity_score y categorías
    """
    response = requests.post(
        API_URL,
        headers={
            "X-API-Key": API_KEY,
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

def debe_bloquear(resultado: dict, umbral: float = 0.7) -> bool:
    """
    Determina si un contenido debe ser bloqueado.
    
    Args:
        resultado: Respuesta de moderar_contenido()
        umbral: Puntuación mínima para bloquear (default 0.7)
    
    Returns:
        True si debe bloquearse, False si puede publicarse
    """
    # Bloquear si toxicidad general supera umbral
    if resultado['toxicity_score'] >= umbral:
        return True
    
    # Bloquear si hay amenazas o ataques de identidad (tolerancia cero)
    categorias = resultado['categories']
    if categorias.get('threat', 0) >= 0.5:
        return True
    if categorias.get('identity_attack', 0) >= 0.5:
        return True
    
    return False

# Ejemplo de uso
texto_usuario = "Gracias por tu ayuda, eres genial!"
resultado = moderar_contenido(texto_usuario)

if debe_bloquear(resultado):
    print("❌ BLOQUEADO - Contenido inapropiado")
    print(f"   Razón: Toxicidad {resultado['toxicity_score']:.0%}")
else:
    print("✅ APROBADO - Contenido apropiado")
    print(f"   Toxicidad: {resultado['toxicity_score']:.0%}")

# Output:
# ✅ APROBADO - Contenido apropiado
#    Toxicidad: 2%
```

### JavaScript / Node.js

```javascript
const API_URL = 'https://apisdom.com/api/v1/moderacion';
const API_KEY = 'tu_api_key_aqui';

async function moderarContenido(texto) {
  /**
   * Analiza un texto para detectar contenido tóxico.
   * @param {string} texto - Texto a moderar (máx 5000 caracteres)
   * @returns {Promise<Object>} - Resultado con is_toxic, toxicity_score, categories
   */
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
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

function debeBloquear(resultado, umbral = 0.7) {
  /**
   * Determina si un contenido debe ser bloqueado.
   */
  if (resultado.toxicity_score >= umbral) return true;
  if (resultado.categories.threat >= 0.5) return true;
  if (resultado.categories.identity_attack >= 0.5) return true;
  return false;
}

// Ejemplo de uso con async/await
async function procesarComentario(comentario) {
  try {
    const resultado = await moderarContenido(comentario);
    
    if (debeBloquear(resultado)) {
      console.log('❌ Comentario bloqueado');
      console.log(`   Toxicidad: ${(resultado.toxicity_score * 100).toFixed(0)}%`);
      
      // Identificar la razón principal
      const categorias = resultado.categories;
      const razon = Object.entries(categorias)
        .filter(([_, score]) => score >= 0.5)
        .sort((a, b) => b[1] - a[1])
        .map(([cat, score]) => `${cat}: ${(score * 100).toFixed(0)}%`);
      
      if (razon.length > 0) {
        console.log(`   Detalle: ${razon.join(', ')}`);
      }
      
      return { aprobado: false, razon: resultado };
    } else {
      console.log('✅ Comentario aprobado');
      return { aprobado: true };
    }
  } catch (error) {
    console.error('Error moderando:', error.message);
    throw error;
  }
}

// Ejemplo
procesarComentario('Este tutorial es muy útil, gracias por compartir!');
// Output: ✅ Comentario aprobado
```

### cURL

```bash
# Ejemplo básico
curl -X POST "https://apisdom.com/api/v1/moderacion" \
  -H "X-API-Key: tu_api_key_aqui" \
  -H "Content-Type: application/json" \
  -d '{"text": "Excelente artículo, muy bien explicado."}'

# Con jq para formatear la respuesta
curl -s -X POST "https://apisdom.com/api/v1/moderacion" \
  -H "X-API-Key: tu_api_key_aqui" \
  -H "Content-Type: application/json" \
  -d '{"text": "Este contenido de ejemplo es totalmente inocente."}' | jq .
```

### PHP

```php
<?php
$api_url = 'https://apisdom.com/api/v1/moderacion';
$api_key = 'tu_api_key_aqui';

function moderarContenido($texto) {
    global $api_url, $token;
    
    $ch = curl_init($api_url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'X-API-Key: ' . $api_key,
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

function debeBloquear($resultado, $umbral = 0.7) {
    if ($resultado['toxicity_score'] >= $umbral) return true;
    if ($resultado['categories']['threat'] >= 0.5) return true;
    if ($resultado['categories']['identity_attack'] >= 0.5) return true;
    return false;
}

// Ejemplo de uso en un formulario
$comentario = $_POST['comentario'] ?? 'Texto de prueba amigable';

try {
    $resultado = moderarContenido($comentario);
    
    if (debeBloquear($resultado)) {
        echo "❌ Tu comentario no puede ser publicado.\n";
        echo "Razón: Contenido potencialmente ofensivo detectado.\n";
    } else {
        echo "✅ Comentario publicado correctamente.\n";
        // Aquí guardarías el comentario en la base de datos
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
?>
```

### C# / .NET

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

public class ModerationApiClient
{
    private readonly HttpClient _client;
    private const string API_URL = "https://apisdom.com/api/v1/moderacion";

    public ModerationApiClient(string apiKey)
    {
        _client = new HttpClient();
        _client.DefaultRequestHeaders.Add("X-API-Key", apiKey);
    }

    public async Task<ModerationResult> ModerarContenidoAsync(string texto)
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
        var options = new JsonSerializerOptions 
        { 
            PropertyNameCaseInsensitive = true 
        };
        return JsonSerializer.Deserialize<ModerationResult>(json, options);
    }

    public bool DebeBloquear(ModerationResult resultado, double umbral = 0.7)
    {
        if (resultado.ToxicityScore >= umbral) return true;
        if (resultado.Categories.Threat >= 0.5) return true;
        if (resultado.Categories.IdentityAttack >= 0.5) return true;
        return false;
    }
}

public class ModerationResult
{
    public string Text { get; set; }
    
    [JsonPropertyName("is_toxic")]
    public bool IsToxic { get; set; }
    
    [JsonPropertyName("toxicity_score")]
    public double ToxicityScore { get; set; }
    
    public ToxicityCategories Categories { get; set; }
    
    public string? Warning { get; set; }
    
    [JsonPropertyName("info_message")]
    public string? InfoMessage { get; set; }
}

public class ToxicityCategories
{
    public double Toxicity { get; set; }
    
    [JsonPropertyName("severe_toxicity")]
    public double SevereToxicity { get; set; }
    
    public double Obscene { get; set; }
    public double Threat { get; set; }
    public double Insult { get; set; }
    
    [JsonPropertyName("identity_attack")]
    public double IdentityAttack { get; set; }
    
    [JsonPropertyName("sexual_explicit")]
    public double SexualExplicit { get; set; }
}

// Ejemplo de uso
var client = new ModerationApiClient("tu_api_key_aqui");
var resultado = await client.ModerarContenidoAsync("Gracias por la información!");

if (client.DebeBloquear(resultado))
{
    Console.WriteLine($"❌ Bloqueado - Toxicidad: {resultado.ToxicityScore:P0}");
}
else
{
    Console.WriteLine($"✅ Aprobado - Toxicidad: {resultado.ToxicityScore:P0}");
}
```

---

## 📊 Casos de Uso Prácticos

### 1. Sistema de Moderación de Comentarios

```python
class SistemaModeración:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://apisdom.com/api/v1/moderacion"
    
    def evaluar(self, texto):
        """Evalúa un texto y devuelve la acción recomendada."""
        resultado = self._llamar_api(texto)
        
        # Clasificar según severidad
        if resultado['categories']['severe_toxicity'] >= 0.6:
            return {
                'accion': 'BLOQUEAR_USUARIO',
                'razon': 'Contenido severamente tóxico',
                'notificar_admin': True
            }
        elif resultado['categories']['threat'] >= 0.5:
            return {
                'accion': 'BLOQUEAR_Y_REVISAR',
                'razon': 'Amenaza detectada',
                'notificar_admin': True
            }
        elif resultado['toxicity_score'] >= 0.7:
            return {
                'accion': 'RECHAZAR',
                'razon': 'Contenido tóxico',
                'notificar_admin': False
            }
        elif resultado['toxicity_score'] >= 0.4:
            return {
                'accion': 'COLA_REVISION',
                'razon': 'Contenido dudoso - requiere revisión humana',
                'notificar_admin': False
            }
        else:
            return {
                'accion': 'APROBAR',
                'razon': None,
                'notificar_admin': False
            }
    
    def _llamar_api(self, texto):
        # ... implementación de la llamada HTTP
        pass

# Uso
moderador = SistemaModeración("tu_api_key_aqui")
resultado = moderador.evaluar("Tu comentario aquí")
print(f"Acción: {resultado['accion']}")
```

### 2. Chat en Tiempo Real con Filtro

```javascript
class ChatModerado {
  constructor(token) {
    this.token = token;
    this.historialUsuario = new Map(); // Para tracking de usuarios
  }

  async procesarMensaje(userId, mensaje) {
    const resultado = await moderarContenido(mensaje);
    
    // Actualizar historial del usuario
    const historial = this.historialUsuario.get(userId) || { infracciones: 0 };
    
    if (resultado.is_toxic) {
      historial.infracciones++;
      this.historialUsuario.set(userId, historial);
      
      if (historial.infracciones >= 3) {
        return {
          publicar: false,
          accion: 'SILENCIAR_USUARIO',
          mensaje: 'Has sido silenciado por comportamiento inapropiado.'
        };
      }
      
      return {
        publicar: false,
        accion: 'RECHAZAR_MENSAJE',
        mensaje: `Mensaje rechazado (Advertencia ${historial.infracciones}/3)`
      };
    }
    
    return {
      publicar: true,
      accion: null,
      mensaje: mensaje
    };
  }
}

// Ejemplo en un servidor WebSocket
const chat = new ChatModerado('tu_api_key_aqui');

socket.on('nuevo_mensaje', async (data) => {
  const resultado = await chat.procesarMensaje(data.userId, data.texto);
  
  if (resultado.publicar) {
    io.emit('mensaje', { user: data.userId, texto: data.texto });
  } else {
    socket.emit('error', { mensaje: resultado.mensaje });
  }
});
```

### 3. Análisis de Reportes de la Comunidad

```python
def generar_reporte_moderacion(comentarios):
    """
    Analiza una lista de comentarios y genera un reporte.
    
    Args:
        comentarios: Lista de dicts con {id, autor, texto}
    
    Returns:
        Reporte con estadísticas y contenido problemático
    """
    resultados = []
    
    for comentario in comentarios:
        moderacion = moderar_contenido(comentario['texto'])
        resultados.append({
            **comentario,
            'moderacion': moderacion
        })
    
    # Generar estadísticas
    total = len(resultados)
    toxicos = sum(1 for r in resultados if r['moderacion']['is_toxic'])
    
    # Identificar los peores infractores
    por_autor = {}
    for r in resultados:
        autor = r['autor']
        if autor not in por_autor:
            por_autor[autor] = {'total': 0, 'toxicos': 0}
        por_autor[autor]['total'] += 1
        if r['moderacion']['is_toxic']:
            por_autor[autor]['toxicos'] += 1
    
    infractores = [
        {'autor': k, **v, 'ratio': v['toxicos']/v['total']}
        for k, v in por_autor.items()
        if v['toxicos'] >= 2
    ]
    infractores.sort(key=lambda x: x['ratio'], reverse=True)
    
    return {
        'resumen': {
            'total_comentarios': total,
            'comentarios_toxicos': toxicos,
            'porcentaje_toxicidad': f"{(toxicos/total)*100:.1f}%"
        },
        'infractores_frecuentes': infractores[:10],
        'comentarios_bloqueados': [
            r for r in resultados 
            if r['moderacion']['toxicity_score'] >= 0.7
        ]
    }

# Ejemplo
reporte = generar_reporte_moderacion(lista_comentarios)
print(f"📊 Toxicidad en la comunidad: {reporte['resumen']['porcentaje_toxicidad']}")
```

---

## ⚠️ Códigos de Error

| Código | Significado | Solución |
|--------|-------------|----------|
| `400` | Texto inválido (vacío o muy largo) | Asegúrate de enviar entre 1 y 5000 caracteres |
| `401` | Token inválido o expirado | Obtén un nuevo token desde el dashboard |
| `402` | Sin créditos disponibles | Recarga tu saldo en apisdom.com |
| `429` | Límite de peticiones excedido | Espera antes de reintentar |
| `500` | Error interno del servidor | Reintenta en unos segundos |

---

## � Transparencia Técnica

> **Política de Apisdom**: Creemos que los desarrolladores merecen saber exactamente cómo funcionan las APIs que usan. Esta sección documenta los detalles técnicos verificados directamente del código fuente.

### Cómo Funciona Internamente

```
Tu texto → Tokenización (toxic-bert) → Inferencia → Cálculo → Respuesta
         ↓                            ↓            ↓
         512 tokens máx           CPU-bound    max_score > 0.7 = is_toxic
                                  (threadpool)
```

### Detalles Verificados del Código

| Aspecto | Valor Real | Archivo Fuente |
|---------|------------|----------------|
| **Modelo** | `unitary/toxic-bert` | moderation_service.py línea 28 |
| **Pipeline** | `text-classification` de HuggingFace | moderation_service.py |
| **Truncamiento** | 512 tokens (código: `text[:512]`) | moderation_service.py línea 45 |
| **Threshold is_toxic** | `max_score > 0.7` | moderation_service.py línea 71 |
| **Ejecución** | `run_in_threadpool` (no bloquea async) | moderation_service.py |

### Cálculo de `is_toxic` y `toxicity_score`

```python
# Código real simplificado (moderation_service.py)
for result in results:
    label = result["label"].lower()
    score = float(result["score"])
    categories[label] = score
    max_score = max(max_score, score)

is_toxic = max_score > 0.7  # Threshold fijo
toxicity_score = round(max_score, 3)
```

**Implicación**: `is_toxic` es una **simplificación binaria** basada en el score más alto. Si necesitas umbrales personalizados, usa `toxicity_score` directamente en tu lógica.

### Créditos: Flujo Real

```
1. Verificar créditos ANTES de ejecutar modelo (CreditChecker.check_credits)
   ↓ Si no hay créditos → HTTP 402 (modelo NO ejecutado, CPU no consumida)
   
2. Ejecutar inferencia toxic-bert
   
3. Consumir crédito DESPUÉS de éxito (CreditChecker.consume_credit)
   ↓ + Registrar uso en Redis para analytics
```

### Por Qué `categories` Puede Variar

El modelo `unitary/toxic-bert` retorna **solo las etiquetas que detecta con confianza**. No siempre devuelve todas las categorías. Tu código debe:

```python
# ❌ INCORRECTO - Puede fallar con KeyError
if resultado['categories']['threat'] >= 0.5:

# ✅ CORRECTO - Usa .get() con default
if resultado['categories'].get('threat', 0) >= 0.5:
```

---

## �📝 Notas Importantes

### Umbrales Recomendados por Tipo de Plataforma

| Tipo de Plataforma | Umbral Toxicidad | Umbral Amenazas | Umbral Identidad |
|-------------------|------------------|-----------------|------------------|
| Foro para niños | 0.3 | 0.2 | 0.2 |
| Red social general | 0.5 | 0.4 | 0.4 |
| Foro de adultos | 0.7 | 0.4 | 0.5 |
| Chat privado | 0.8 | 0.5 | 0.6 |

### Sobre Falsos Positivos

El modelo puede marcar como tóxico:
- Discusiones sobre temas sensibles (política, religión)
- Citas de contenido tóxico para criticarlo
- Sarcasmo o humor negro

**Recomendación**: Para contenido cerca del umbral (0.4-0.7), implementa revisión humana.

### Idiomas Soportados

El modelo `unitary/toxic-bert` fue entrenado principalmente en inglés:
- ✅ **Inglés**: Rendimiento óptimo
- ⚠️ **Español y otros idiomas**: Funciona pero con precisión reducida

**Nota honesta:** Si tu contenido es principalmente en español, el modelo puede tener más falsos negativos (contenido tóxico no detectado) o falsos positivos.

---

## 🔗 Recursos Relacionados

- [Sentiment API](./SENTIMENT_API.md) - Análisis de sentimiento
- [Prediction API](./PREDICTION_API.md) - Predicciones de series temporales

---

## 💬 ¿Necesitas Ayuda?

📧 soporte@apisdom.com
