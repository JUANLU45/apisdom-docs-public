# Apisdom JavaScript Examples

Ejemplos de uso de las APIs de Apisdom en JavaScript/Node.js.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `apisdom-client.js` | Cliente completo con retry y manejo de errores |

## Uso en Navegador

```html
<script src="apisdom-client.js"></script>
<script>
  const client = new ApisdClient('tu_api_key');
  
  client.analizarSentimiento('¡Excelente producto!')
    .then(r => console.log(r.sentiment))
    .catch(e => console.error(e));
</script>
```

## Uso en Node.js

```javascript
const { ApisdClient, CreditosInsuficientesError } = require('./apisdom-client');

const client = new ApisdClient('tu_api_key');

async function main() {
  try {
    const resultado = await client.analizarSentimiento('¡Me encanta!');
    console.log(`${resultado.sentiment}: ${resultado.score * 100}%`);
  } catch (error) {
    if (error instanceof CreditosInsuficientesError) {
      console.log('Recarga créditos en apisdom.com');
    }
  }
}

main();
```

## Características

- ✅ Retry automático con backoff exponencial
- ✅ Manejo de rate limit (429)
- ✅ Excepciones específicas para créditos (402) y token (401)
- ✅ Compatible con navegador y Node.js
- ✅ JSDoc para autocompletado en IDEs

## TypeScript

El archivo incluye typedefs JSDoc. Para TypeScript completo, crea un archivo `.d.ts`:

```typescript
declare class ApisdClient {
  constructor(apiKey: string, baseUrl?: string);
  analizarSentimiento(texto: string): Promise<SentimentResponse>;
  moderarContenido(texto: string): Promise<ModerationResponse>;
  predecirSerie(dates: string[], values: number[], periods?: number): Promise<PredictionResponse>;
}

interface SentimentResponse {
  text: string;
  sentiment: 'positive' | 'negative';  // Modelo binario SST-2
  score: number;
  warning: string | null;
}

interface ModerationResponse {
  text: string;
  is_toxic: boolean;
  toxicity_score: number;
  categories: Record<string, number>;
}

interface PredictionResponse {
  predictions: Array<{ date: string; value: number }>;
  mape: number;
  quality_warning: string | null;
}
```

## Documentación

- [Sentiment API](../../docs/SENTIMENT_API.md)
- [Moderation API](../../docs/MODERATION_API.md)
- [Prediction API](../../docs/PREDICTION_API.md)
