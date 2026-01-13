# 📈 Prediction API

**Predicción de Series Temporales con Inteligencia Artificial**

Genera predicciones precisas para datos históricos como ventas, tráfico web, inventario, métricas de negocio y cualquier serie temporal. Usa el motor NeuralProphet, una evolución de Facebook Prophet con redes neuronales.

---

## 📍 Información General

| Propiedad | Valor |
|-----------|-------|
| **URL Base** | `https://api.apisdom.com/api/v1/prediction` |
| **Método** | `POST` |
| **Autenticación** | Bearer Token (JWT) |
| **Tipo de Crédito** | `prediction` |
| **Coste por llamada** | 1 crédito |
| **Modelo IA** | NeuralProphet (neural network forecasting) |
| **Horizonte máximo** | 365 días/periodos |

---

## 🔐 Autenticación

Todas las peticiones requieren un token JWT en el header `Authorization`:

```
Authorization: Bearer tu_token_jwt_aqui
```

Puedes obtener tu token desde el panel de usuario en [apisdom.com/dashboard](https://apisdom.com/dashboard).

---

## 📥 Endpoint: Generar Predicción

```
POST /api/v1/prediction/forecast
```

### Request Body

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `dates` | string[] | ✅ Sí | - | Lista de fechas en formato `YYYY-MM-DD`. Mínimo 10, máximo 5000. |
| `values` | float[] | ✅ Sí | - | Lista de valores numéricos correspondientes. Debe tener la misma longitud que `dates`. |
| `periods` | int | ❔ Opcional | 7 | Número de periodos futuros a predecir. Mínimo 1, máximo 365. |

### Validaciones Importantes

- `dates` y `values` deben tener **exactamente la misma longitud**
- Mínimo **10 puntos de datos** (para entrenar el modelo correctamente)
- Máximo **5000 puntos de datos**
- Fechas deben estar en **orden cronológico**
- Los valores pueden ser enteros o decimales

### Ejemplo de Request

```json
{
  "dates": [
    "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10",
    "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15"
  ],
  "values": [
    120.5, 135.2, 128.7, 142.1, 155.3,
    148.9, 160.0, 172.4, 165.8, 180.2,
    175.6, 188.9, 195.3, 201.7, 210.5
  ],
  "periods": 7
}
```

### Response Exitosa (200 OK)

```json
{
  "predictions": [
    {"date": "2024-01-16", "value": 218.34, "lower": 218.34, "upper": 218.34},
    {"date": "2024-01-17", "value": 225.12, "lower": 225.12, "upper": 225.12},
    {"date": "2024-01-18", "value": 231.89, "lower": 231.89, "upper": 231.89},
    {"date": "2024-01-19", "value": 238.45, "lower": 238.45, "upper": 238.45},
    {"date": "2024-01-20", "value": 245.01, "lower": 245.01, "upper": 245.01},
    {"date": "2024-01-21", "value": 251.78, "lower": 251.78, "upper": 251.78},
    {"date": "2024-01-22", "value": 258.34, "lower": 258.34, "upper": 258.34}
  ],
  "quality_warning": null,
  "mape": 0.042,
  "info_message": null
}
```

> **Nota:** Actualmente `lower` y `upper` tienen el mismo valor que `value`. Estos campos están reservados para futura implementación de intervalos de confianza.
```

### Campos de la Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `predictions` | array | Lista de predicciones con fecha y valor |
| `predictions[].date` | string | Fecha predicha en formato `YYYY-MM-DD` |
| `predictions[].value` | float | Valor predicho para esa fecha |
| `predictions[].lower` | float | Límite inferior (reservado para intervalos de confianza) |
| `predictions[].upper` | float | Límite superior (reservado para intervalos de confianza) |
| `quality_warning` | string \| null | Aviso si MAPE > 40% (datos insuficientes o erráticos) |
| `mape` | float | Mean Absolute Percentage Error (0.0-1.0, donde 0.05 = 5% error) |
| `info_message` | string \| null | Mensaje informativo para usuarios del plan gratuito |

### Interpretando el MAPE

El MAPE (Mean Absolute Percentage Error) se devuelve como valor decimal (0.0 a 1.0):

| MAPE (valor) | Error (%) | Interpretación | Confiabilidad |
|--------------|-----------|----------------|---------------|
| < 0.05 | < 5% | Excelente | ⭐⭐⭐⭐⭐ Muy alta |
| 0.05-0.10 | 5-10% | Bueno | ⭐⭐⭐⭐ Alta |
| 0.10-0.20 | 10-20% | Aceptable | ⭐⭐⭐ Media |
| 0.20-0.40 | 20-40% | Regular | ⭐⭐ Baja |
| > 0.40 | > 40% | Deficiente | ⭐ Muy baja - Verás `quality_warning` |

---

## 💻 Ejemplos de Código

### Python

```python
import requests
from datetime import datetime, timedelta
from typing import List

API_URL = "https://api.apisdom.com/api/v1/prediction/forecast"
TOKEN = "tu_token_jwt_aqui"

def predecir(
    fechas: List[str], 
    valores: List[float], 
    periodos: int
) -> dict:
    """
    Genera predicciones para una serie temporal.
    
    Args:
        fechas: Lista de fechas en formato 'YYYY-MM-DD'
        valores: Lista de valores numéricos
        periodos: Número de periodos futuros a predecir (1-365)
    
    Returns:
        dict con predictions, quality_warning y mape
    """
    if len(fechas) != len(valores):
        raise ValueError("fechas y valores deben tener la misma longitud")
    if len(fechas) < 10:
        raise ValueError("Se necesitan al menos 10 puntos de datos")
    if not 1 <= periodos <= 365:
        raise ValueError("periodos debe estar entre 1 y 365")
    
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "dates": fechas,
            "values": valores,
            "periods": periodos
        }
    )
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 402:
        raise Exception("Sin créditos. Recarga tu saldo en apisdom.com")
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Ejemplo: Predecir ventas de las próximas 2 semanas
ventas_historicas = {
    "fechas": [f"2024-{mes:02d}-{dia:02d}" 
               for mes in range(1, 4) 
               for dia in range(1, 29)],
    "valores": [
        # Enero (tendencia al alza)
        100, 105, 98, 112, 120, 115, 95,  # Semana 1
        108, 118, 125, 130, 128, 122, 100, # Semana 2
        115, 128, 135, 140, 138, 132, 108, # Semana 3
        125, 138, 145, 150, 148, 142, 118, # Semana 4
        # Febrero (estacionalidad)
        120, 125, 118, 132, 140, 135, 110,
        128, 138, 145, 150, 148, 142, 115,
        135, 148, 155, 160, 158, 152, 125,
        145, 158, 165, 170, 168, 162, 135,
        # Marzo (pico)
        140, 145, 138, 152, 165, 160, 132,
        150, 162, 170, 178, 175, 168, 142,
        160, 175, 185, 192, 188, 180, 155,
        172, 188, 198, 205, 200, 192, 165,
    ]
}

resultado = predecir(
    ventas_historicas["fechas"][:84],  # 84 días de datos
    ventas_historicas["valores"][:84],
    periodos=14  # Predecir 2 semanas
)

print(f"📊 Predicciones generadas")
print(f"   Margen de error (MAPE): {resultado['mape']:.1f}%")
print(f"\n📅 Próximas 14 días:")
for pred in resultado['predictions']:
    print(f"   {pred['date']}: {pred['value']:.2f}")

# Output:
# 📊 Predicciones generadas
#    Margen de error (MAPE): 7.3%
# 
# 📅 Próximas 14 días:
#    2024-03-25: 185.34
#    2024-03-26: 201.12
#    ... etc
```

### JavaScript / Node.js

```javascript
const API_URL = 'https://api.apisdom.com/api/v1/prediction/forecast';
const TOKEN = 'tu_token_jwt_aqui';

async function predecir(fechas, valores, periodos) {
  /**
   * Genera predicciones para una serie temporal.
   * @param {string[]} fechas - Lista de fechas 'YYYY-MM-DD'
   * @param {number[]} valores - Lista de valores numéricos
   * @param {number} periodos - Periodos a predecir (1-365)
   * @returns {Promise<Object>} - Predicciones con MAPE
   */
  if (fechas.length !== valores.length) {
    throw new Error('fechas y valores deben tener la misma longitud');
  }
  if (fechas.length < 10) {
    throw new Error('Se necesitan al menos 10 puntos de datos');
  }
  if (periodos < 1 || periodos > 365) {
    throw new Error('periodos debe estar entre 1 y 365');
  }

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ dates: fechas, values: valores, periods: periodos })
  });

  if (response.status === 402) {
    throw new Error('Sin créditos. Recarga tu saldo en apisdom.com');
  }

  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  return response.json();
}

// Ejemplo: Predecir tráfico web
async function predecirTraficoWeb() {
  // Datos de los últimos 30 días
  const fechas = [];
  const valores = [];
  const hoy = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const fecha = new Date(hoy);
    fecha.setDate(fecha.getDate() - i);
    fechas.push(fecha.toISOString().split('T')[0]);
    
    // Simular tráfico con patrón semanal
    const diaSemana = fecha.getDay();
    const baseTrafico = 1000 + Math.random() * 200;
    const factorSemanal = diaSemana === 0 || diaSemana === 6 ? 0.6 : 1.0;
    valores.push(Math.round(baseTrafico * factorSemanal));
  }
  
  try {
    const resultado = await predecir(fechas, valores, 7);
    
    console.log('📈 Predicción de tráfico web');
    console.log(`   Precisión del modelo: ${(100 - resultado.mape).toFixed(1)}%`);
    console.log('\n📅 Próxima semana:');
    
    resultado.predictions.forEach(p => {
      const fecha = new Date(p.date);
      const dia = fecha.toLocaleDateString('es-ES', { weekday: 'short', day: '2-digit' });
      console.log(`   ${dia}: ${Math.round(p.value).toLocaleString()} visitas`);
    });
    
    if (resultado.quality_warning) {
      console.log(`\n⚠️ Advertencia: ${resultado.quality_warning}`);
    }
    
    return resultado;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Ejecutar
predecirTraficoWeb();
```

### cURL

```bash
# Predicción básica con 10 puntos de datos mínimos
curl -X POST "https://api.apisdom.com/api/v1/prediction/forecast" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "dates": [
      "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
      "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10"
    ],
    "values": [100, 105, 102, 108, 115, 112, 120, 118, 125, 130],
    "periods": 5
  }'

# Con jq para formatear
curl -s -X POST "https://api.apisdom.com/api/v1/prediction/forecast" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -H "Content-Type: application/json" \
  -d @datos_ventas.json | jq '.predictions'
```

### PHP

```php
<?php
$api_url = 'https://api.apisdom.com/api/v1/prediction/forecast';
$token = 'tu_token_jwt_aqui';

function predecir($fechas, $valores, $periodos) {
    global $api_url, $token;
    
    // Validaciones
    if (count($fechas) !== count($valores)) {
        throw new Exception('fechas y valores deben tener la misma longitud');
    }
    if (count($fechas) < 10) {
        throw new Exception('Se necesitan al menos 10 puntos de datos');
    }
    if ($periodos < 1 || $periodos > 365) {
        throw new Exception('periodos debe estar entre 1 y 365');
    }
    
    $ch = curl_init($api_url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $token,
            'Content-Type: application/json'
        ],
        CURLOPT_POSTFIELDS => json_encode([
            'dates' => $fechas,
            'values' => $valores,
            'periods' => $periodos
        ])
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 402) {
        throw new Exception('Sin créditos. Recarga tu saldo en apisdom.com');
    }
    
    if ($httpCode !== 200) {
        throw new Exception("Error HTTP: $httpCode");
    }
    
    return json_decode($response, true);
}

// Ejemplo: Predecir ventas mensuales
$fechas = [];
$valores = [];

// Generar 90 días de datos históricos
$fecha_inicio = strtotime('-90 days');
for ($i = 0; $i < 90; $i++) {
    $fecha = date('Y-m-d', strtotime("+$i days", $fecha_inicio));
    $fechas[] = $fecha;
    
    // Simular ventas con tendencia y ruido
    $tendencia = 500 + ($i * 2); // Crecimiento diario
    $ruido = rand(-50, 50);
    $valores[] = $tendencia + $ruido;
}

try {
    $resultado = predecir($fechas, $valores, 30);
    
    echo "📊 Predicción de ventas\n";
    echo "   Error estimado (MAPE): {$resultado['mape']}%\n\n";
    
    echo "📅 Próximos 30 días:\n";
    $total_predicho = 0;
    foreach ($resultado['predictions'] as $pred) {
        $valor_formateado = number_format($pred['value'], 0, ',', '.');
        echo "   {$pred['date']}: \${$valor_formateado}\n";
        $total_predicho += $pred['value'];
    }
    
    echo "\n💰 Total proyectado: $" . number_format($total_predicho, 0, ',', '.') . "\n";
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

### C# / .NET

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

public class PredictionApiClient
{
    private readonly HttpClient _client;
    private const string API_URL = "https://api.apisdom.com/api/v1/prediction/forecast";

    public PredictionApiClient(string token)
    {
        _client = new HttpClient();
        _client.DefaultRequestHeaders.Add("Authorization", $"Bearer {token}");
    }

    public async Task<PredictionResult> PredecirAsync(
        List<string> fechas, 
        List<double> valores, 
        int periodos)
    {
        // Validaciones
        if (fechas.Count != valores.Count)
            throw new ArgumentException("fechas y valores deben tener la misma longitud");
        if (fechas.Count < 10)
            throw new ArgumentException("Se necesitan al menos 10 puntos de datos");
        if (periodos < 1 || periodos > 365)
            throw new ArgumentException("periodos debe estar entre 1 y 365");

        var request = new
        {
            dates = fechas,
            values = valores,
            periods = periodos
        };

        var content = new StringContent(
            JsonSerializer.Serialize(request),
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
        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        return JsonSerializer.Deserialize<PredictionResult>(json, options);
    }
}

public class PredictionResult
{
    public List<Prediction> Predictions { get; set; }
    
    [JsonPropertyName("quality_warning")]
    public string? QualityWarning { get; set; }
    
    public double Mape { get; set; }
    
    [JsonPropertyName("info_message")]
    public string? InfoMessage { get; set; }
}

public class Prediction
{
    public string Date { get; set; }
    public double Value { get; set; }
}

// Ejemplo de uso
var client = new PredictionApiClient("tu_token_jwt_aqui");

// Generar datos de ejemplo (últimos 60 días)
var fechas = new List<string>();
var valores = new List<double>();
var hoy = DateTime.Today;

for (int i = 59; i >= 0; i--)
{
    var fecha = hoy.AddDays(-i);
    fechas.Add(fecha.ToString("yyyy-MM-dd"));
    valores.Add(1000 + (60 - i) * 10 + new Random().Next(-50, 50));
}

var resultado = await client.PredecirAsync(fechas, valores, 14);

Console.WriteLine($"📈 Predicción generada (MAPE: {resultado.Mape:F1}%)");
foreach (var pred in resultado.Predictions)
{
    Console.WriteLine($"   {pred.Date}: {pred.Value:N2}");
}
```

---

## 📊 Casos de Uso Prácticos

### 1. Sistema de Predicción de Ventas

```python
class PredictorVentas:
    """Sistema completo de predicción de ventas."""
    
    def __init__(self, token):
        self.token = token
    
    def predecir_y_analizar(self, datos_historicos, dias_futuro=30):
        """
        Genera predicción y análisis de tendencia.
        
        Args:
            datos_historicos: dict con 'fechas' y 'valores'
            dias_futuro: número de días a predecir
        
        Returns:
            dict con predicciones y análisis
        """
        resultado = predecir(
            datos_historicos['fechas'],
            datos_historicos['valores'],
            dias_futuro
        )
        
        # Calcular métricas adicionales
        valores_historicos = datos_historicos['valores']
        valores_predichos = [p['value'] for p in resultado['predictions']]
        
        promedio_historico = sum(valores_historicos) / len(valores_historicos)
        promedio_predicho = sum(valores_predichos) / len(valores_predichos)
        
        cambio_porcentual = ((promedio_predicho - promedio_historico) / promedio_historico) * 100
        
        # Detectar tendencia
        if cambio_porcentual > 10:
            tendencia = "📈 CRECIMIENTO FUERTE"
        elif cambio_porcentual > 3:
            tendencia = "📈 Crecimiento moderado"
        elif cambio_porcentual > -3:
            tendencia = "➡️ Estable"
        elif cambio_porcentual > -10:
            tendencia = "📉 Descenso moderado"
        else:
            tendencia = "📉 DESCENSO FUERTE"
        
        return {
            'predicciones': resultado['predictions'],
            'mape': resultado['mape'],
            'analisis': {
                'tendencia': tendencia,
                'cambio_porcentual': f"{cambio_porcentual:+.1f}%",
                'promedio_historico': promedio_historico,
                'promedio_predicho': promedio_predicho,
                'total_proyectado': sum(valores_predichos)
            }
        }
    
    def generar_reporte(self, datos, dias=30):
        """Genera un reporte formateado."""
        resultado = self.predecir_y_analizar(datos, dias)
        
        print("═" * 50)
        print("📊 REPORTE DE PREDICCIÓN DE VENTAS")
        print("═" * 50)
        print(f"Tendencia: {resultado['analisis']['tendencia']}")
        print(f"Cambio esperado: {resultado['analisis']['cambio_porcentual']}")
        print(f"Precisión del modelo: {100 - resultado['mape']:.1f}%")
        print(f"\n💰 Total proyectado ({dias} días): ${resultado['analisis']['total_proyectado']:,.2f}")
        print("═" * 50)
        
        return resultado

# Uso
predictor = PredictorVentas("tu_token_jwt_aqui")
reporte = predictor.generar_reporte(datos_ventas, 30)
```

### 2. Predicción de Inventario con Alertas

```javascript
async function predecirInventario(productoId, stockActual, ventasHistoricas) {
  /**
   * Predice cuándo se agotará el inventario y recomienda reabastecimiento.
   */
  const resultado = await predecir(
    ventasHistoricas.fechas,
    ventasHistoricas.valores,
    30  // Predecir 30 días
  );
  
  // Simular consumo de inventario
  let stockRestante = stockActual;
  let diasHastaAgotarse = null;
  let fechaAgotamiento = null;
  
  for (let i = 0; i < resultado.predictions.length; i++) {
    const pred = resultado.predictions[i];
    stockRestante -= pred.value;
    
    if (stockRestante <= 0 && diasHastaAgotarse === null) {
      diasHastaAgotarse = i + 1;
      fechaAgotamiento = pred.date;
    }
  }
  
  // Calcular nivel de alerta
  let alerta;
  if (diasHastaAgotarse !== null && diasHastaAgotarse <= 7) {
    alerta = { nivel: 'CRÍTICO', emoji: '🔴', mensaje: '¡Reabastecer inmediatamente!' };
  } else if (diasHastaAgotarse !== null && diasHastaAgotarse <= 14) {
    alerta = { nivel: 'ALTO', emoji: '🟠', mensaje: 'Planificar reabastecimiento esta semana' };
  } else if (diasHastaAgotarse !== null && diasHastaAgotarse <= 21) {
    alerta = { nivel: 'MEDIO', emoji: '🟡', mensaje: 'Considerar reabastecimiento pronto' };
  } else {
    alerta = { nivel: 'BAJO', emoji: '🟢', mensaje: 'Stock saludable' };
  }
  
  // Calcular cantidad recomendada
  const ventaDiaria = resultado.predictions.reduce((a, b) => a + b.value, 0) / 30;
  const stockRecomendado = Math.ceil(ventaDiaria * 45); // 45 días de inventario
  const cantidadPedir = Math.max(0, stockRecomendado - stockActual);
  
  return {
    productoId,
    stockActual,
    diasHastaAgotarse,
    fechaAgotamiento,
    alerta,
    recomendacion: {
      cantidadPedir,
      fechaLimitePedido: diasHastaAgotarse 
        ? new Date(Date.now() + (diasHastaAgotarse - 7) * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
        : null
    }
  };
}

// Ejemplo
const analisis = await predecirInventario(
  'PROD-001',
  150,
  { fechas: [...], valores: [...] }
);

console.log(`${analisis.alerta.emoji} Alerta: ${analisis.alerta.nivel}`);
console.log(`   Stock actual: ${analisis.stockActual}`);
console.log(`   Días hasta agotarse: ${analisis.diasHastaAgotarse || 'N/A'}`);
console.log(`   Cantidad a pedir: ${analisis.recomendacion.cantidadPedir}`);
```

### 3. Dashboard de Métricas con Proyecciones

```python
import pandas as pd

def crear_dashboard_metricas(metricas_historicas, nombres_metricas):
    """
    Crea un dashboard con múltiples métricas y sus proyecciones.
    
    Args:
        metricas_historicas: dict con múltiples series temporales
        nombres_metricas: lista de nombres para mostrar
    
    Returns:
        DataFrame con comparativa histórico vs proyectado
    """
    resultados = []
    
    for nombre, datos in zip(nombres_metricas, metricas_historicas.values()):
        try:
            pred = predecir(datos['fechas'], datos['valores'], 7)
            
            # Calcular estadísticas
            historico = datos['valores']
            proyectado = [p['value'] for p in pred['predictions']]
            
            resultados.append({
                'Métrica': nombre,
                'Promedio Histórico': f"{sum(historico)/len(historico):,.1f}",
                'Proyección 7 días': f"{sum(proyectado)/7:,.1f}",
                'Cambio': f"{((sum(proyectado)/7 - sum(historico[-7:])/7) / (sum(historico[-7:])/7)) * 100:+.1f}%",
                'MAPE': f"{pred['mape']:.3f}",  # MAPE es decimal 0.0-1.0
                'Alerta': '⚠️' if pred.get('quality_warning') else '✅'
            })
        except Exception as e:
            resultados.append({
                'Métrica': nombre,
                'Error': str(e)
            })
    
    return pd.DataFrame(resultados)

# Ejemplo
metricas = {
    'ventas': {'fechas': [...], 'valores': [...]},
    'visitas': {'fechas': [...], 'valores': [...]},
    'conversiones': {'fechas': [...], 'valores': [...]},
}

dashboard = crear_dashboard_metricas(
    metricas, 
    ['Ventas ($)', 'Visitas Web', 'Tasa Conversión']
)
print(dashboard.to_string(index=False))

# Output:
# Métrica        Promedio Histórico  Proyección 7 días  Cambio  Error (MAPE)  Alerta
# Ventas ($)           2,345.6           2,567.8       +9.5%       6.2%       ✅
# Visitas Web         12,456.0          13,234.0       +6.2%       8.9%       ✅
# Tasa Conversión          3.2               3.4       +6.3%      12.7%       ⚠️
```

---

## 🔬 Transparencia Técnica

> **Política de Apisdom**: Creemos que los desarrolladores merecen saber exactamente cómo funcionan las APIs que usan. Esta sección documenta los detalles técnicos verificados directamente del código fuente.

### Cómo Funciona Internamente

```
Tus datos → DataFrame → Entrenamiento NeuralProphet → Predicción → Validación MAPE
          ↓            ↓                            ↓             ↓
          pd.DataFrame epochs varían por tier      make_future   si MAPE>0.4 = warning
                       (free=10, pro=50)           dataframe
```

### Detalles Verificados del Código

| Aspecto | Valor Real | Archivo Fuente |
|---------|------------|----------------|
| **Motor** | `NeuralProphet` (no Prophet clásico) | prediction_service.py |
| **Estacionalidad** | `daily=True, weekly=True, yearly=False` | prediction_service.py línea 37 |
| **Epochs Free/Starter** | 10 | prediction_service.py línea 81 |
| **Epochs Pro** | 50 | prediction_service.py línea 81 |
| **Learning rate** | 1.0 | prediction_service.py línea 42 |
| **n_lags** | 0 (autoregresión desactivada) | prediction_service.py línea 40 |
| **Threshold MAPE warning** | 0.4 (40%) | prediction_service.py línea 93 |

### Cálculo del MAPE

```python
# Código real simplificado (prediction_service.py)
def calculate_mape(actual, predicted):
    mask = actual != 0  # Evitar división por cero
    if not mask.any():
        return 1.0  # Si todos son 0, MAPE = 100%
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask]))
```

**Implicación**: Si tus datos históricos tienen muchos ceros, el MAPE puede ser artificialmente alto.

### Epochs: Impacto Real en Calidad

| Plan | Epochs | Impacto |
|------|--------|---------|
| Free/Starter | 10 | Modelo más simple, entrena rápido (~2-5s), MAPE típico +5-10% |
| Pro | 50 | Modelo más refinado, entrena más (~10-15s), mejor precisión |

**Nota honesta**: Para muchos casos de uso, 10 epochs son suficientes. La diferencia se nota principalmente en series con patrones complejos o estacionalidad fuerte.

### Créditos: Flujo Real

```
1. Verificar créditos ANTES de entrenar modelo (CreditChecker.check_credits)
   ↓ Si no hay créditos → HTTP 402 (CPU no consumida)
   
2. Entrenar NeuralProphet con tus datos (CPU-intensive)
   
3. Generar predicciones (make_future_dataframe + predict)

4. Consumir crédito DESPUÉS de éxito (CreditChecker.consume_credit)
```

### Por Qué `lower` y `upper` Son Iguales a `value`

Actualmente NO implementamos intervalos de confianza. Los campos existen para **compatibilidad futura**:

```python
# Código actual retorna:
{"date": "2024-01-16", "value": 218.34, "lower": 218.34, "upper": 218.34}

# Futuro (cuando implementemos quantile regression):
{"date": "2024-01-16", "value": 218.34, "lower": 195.20, "upper": 241.48}
```

---

## ⚠️ Códigos de Error

| Código | Significado | Solución |
|--------|-------------|----------|
| `400` | Datos inválidos | Verifica: mínimo 10 puntos, fechas=valores longitud, periodos 1-365 |
| `401` | Token inválido o expirado | Obtén un nuevo token desde el dashboard |
| `402` | Sin créditos disponibles | Recarga tu saldo en apisdom.com |
| `422` | Error de validación | Revisa formato de fechas (YYYY-MM-DD) y tipos de datos |
| `429` | Límite de peticiones excedido | Espera antes de reintentar |
| `500` | Error interno del servidor | Reintenta en unos segundos |

---

## 📝 Notas Importantes

### Sobre el MAPE

El MAPE (Mean Absolute Percentage Error) se devuelve como **decimal** (0.0 a 1.0):
- `mape: 0.05` = 5% de error (excelente)
- `mape: 0.15` = 15% de error (aceptable)
- `mape: 0.40` = 40% de error (recibirás `quality_warning`)

Para convertir a porcentaje: `mape * 100`

### Sobre la Calidad de las Predicciones

| Factor | Impacto | Recomendación |
|--------|---------|---------------|
| Cantidad de datos | Alto | Mínimo 30 puntos para predicciones confiables |
| Regularidad temporal | Alto | Usa frecuencia consistente (diaria, semanal) |
| Valores atípicos | Medio | Limpia outliers antes de enviar |
| Estacionalidad | Medio | Incluye al menos 1 ciclo completo |
| Tendencia clara | Alto | Series con tendencia tienen mejor MAPE |

### Cuando el `quality_warning` Aparece

Recibirás advertencias cuando:
- Menos de 30 puntos de datos
- Alta variabilidad (coeficiente de variación > 50%)
- Datos con gaps (fechas no consecutivas)
- Valores negativos o ceros frecuentes

### Tiempo de Respuesta

| Puntos de Datos | Tiempo Estimado |
|-----------------|-----------------|
| 10-100 | < 2 segundos |
| 100-1000 | 2-5 segundos |
| 1000-5000 | 5-15 segundos |

**Nota**: La primera petición del día puede tener ~20s de latencia adicional (cold start) en el plan gratuito.

---

## 🔗 Recursos Relacionados

- [Sentiment API](./SENTIMENT_API.md) - Análisis de sentimiento
- [Moderation API](./MODERATION_API.md) - Detección de contenido tóxico

---

## 💬 ¿Necesitas Ayuda?

📧 soporte@apisdom.com
