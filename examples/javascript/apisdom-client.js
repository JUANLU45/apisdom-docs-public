/**
 * Apisdom JavaScript/Node.js Client
 * Cliente robusto con retry y manejo de errores
 * 
 * Documentación: https://github.com/apisdom/docs
 * Versión: 1.0.0
 */

/**
 * Cliente para las APIs de Apisdom
 */
class ApisdClient {
  /**
   * @param {string} apiKey - Tu API Key de apisdom.com/dashboard
   * @param {string} baseUrl - URL base de la API
   */
  constructor(apiKey, baseUrl = 'https://apisdom.com') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  /**
   * Request con retry automático y backoff exponencial
   * @private
   */
  async _requestWithRetry(method, endpoint, body = null, maxRetries = 3) {
    const url = `${this.baseUrl}${endpoint}`;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          method,
          headers: {
            'X-API-Key': this.apiKey,
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
          await this._sleep(retryAfter * 1000);
          continue;
        }

        // Error servidor - Retry con backoff
        if (response.status >= 500) {
          const waitTime = Math.pow(2, attempt) * 1000;
          console.log(`Error ${response.status}. Retry en ${waitTime}ms...`);
          await this._sleep(waitTime);
          continue;
        }

        throw new Error(`HTTP ${response.status}`);

      } catch (error) {
        if (error instanceof CreditosInsuficientesError) throw error;
        if (error instanceof TokenInvalidoError) throw error;
        
        if (attempt < maxRetries - 1) {
          const waitTime = Math.pow(2, attempt) * 2000;
          await this._sleep(waitTime);
          continue;
        }
        throw error;
      }
    }

    throw new Error(`Falló después de ${maxRetries} intentos`);
  }

  /**
   * @private
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Analiza el sentimiento de un texto
   * @param {string} texto - Texto a analizar (máx 5000 caracteres)
   * @returns {Promise<SentimentResponse>}
   */
  async analizarSentimiento(texto) {
    return this._requestWithRetry(
      'POST',
      '/api/v1/sentiment',
      { text: texto }
    );
  }

  /**
   * Detecta contenido tóxico en un texto
   * @param {string} texto - Texto a moderar (máx 5000 caracteres)
   * @returns {Promise<ModerationResponse>}
   */
  async moderarContenido(texto) {
    return this._requestWithRetry(
      'POST',
      '/api/v1/moderacion',
      { text: texto }
    );
  }

  /**
   * Predice valores futuros de una serie temporal
   * @param {string[]} dates - Fechas en formato 'YYYY-MM-DD' (mín 10)
   * @param {number[]} values - Valores numéricos
   * @param {number} periods - Periodos a predecir (1-365)
   * @returns {Promise<PredictionResponse>}
   */
  async predecirSerie(dates, values, periods = 7) {
    if (dates.length !== values.length) {
      throw new Error('dates y values deben tener la misma longitud');
    }
    if (dates.length < 10) {
      throw new Error('Se necesitan al menos 10 puntos de datos');
    }
    if (periods < 1 || periods > 365) {
      throw new Error('periods debe estar entre 1 y 365');
    }

    return this._requestWithRetry(
      'POST',
      '/api/v1/predictions',
      { dates, values, periods }
    );
  }
}

/**
 * Error: Usuario sin créditos
 */
class CreditosInsuficientesError extends Error {
  constructor(message) {
    super(message);
    this.name = 'CreditosInsuficientesError';
  }
}

/**
 * Error: Token inválido o expirado
 */
class TokenInvalidoError extends Error {
  constructor(message) {
    super(message);
    this.name = 'TokenInvalidoError';
  }
}

// TypeScript types (para referencia)
/**
 * @typedef {Object} SentimentResponse
 * @property {string} text - Texto analizado
 * @property {'positive'|'negative'} sentiment - Sentimiento detectado (modelo binario SST-2)
 * @property {number} score - Confianza (0.0 a 1.0)
 * @property {string|null} warning - Aviso si texto truncado
 */

/**
 * @typedef {Object} ModerationResponse
 * @property {string} text - Texto analizado
 * @property {boolean} is_toxic - true si toxicity_score > 0.7
 * @property {number} toxicity_score - Puntuación (0.0 a 1.0)
 * @property {Object} categories - Desglose por categorías
 */

/**
 * @typedef {Object} PredictionResponse
 * @property {Array<{date: string, value: number}>} predictions - Predicciones
 * @property {number} mape - Error porcentual medio
 * @property {string|null} quality_warning - Aviso si MAPE > 40%
 */

// === EJEMPLOS DE USO ===

// Para Node.js, descomenta esta línea:
// module.exports = { ApisdClient, CreditosInsuficientesError, TokenInvalidoError };

// Ejemplo de uso en navegador o Node.js
async function ejemplos() {
  const API_KEY = 'tu_api_key_aqui';
  const client = new ApisdClient(API_KEY);

  console.log('=' .repeat(50));
  console.log('📚 EJEMPLOS DE APISDOM APIs');
  console.log('='.repeat(50));

  // Ejemplo 1: Análisis de sentimiento
  console.log('\n🎭 SENTIMENT API');
  console.log('-'.repeat(40));
  
  try {
    const sentimiento = await client.analizarSentimiento('¡Me encanta este servicio!');
    console.log(`Texto: ${sentimiento.text}`);
    console.log(`Sentimiento: ${sentimiento.sentiment}`);
    console.log(`Confianza: ${(sentimiento.score * 100).toFixed(0)}%`);
  } catch (error) {
    if (error instanceof CreditosInsuficientesError) {
      console.log('⚠️ Sin créditos. Recarga en apisdom.com/dashboard');
    } else {
      console.error('Error:', error.message);
    }
  }

  // Ejemplo 2: Moderación
  console.log('\n🛡️ MODERATION API');
  console.log('-'.repeat(40));
  
  try {
    const moderacion = await client.moderarContenido('Gracias por tu ayuda!');
    console.log(`Texto: ${moderacion.text}`);
    console.log(`¿Tóxico?: ${moderacion.is_toxic ? 'Sí ❌' : 'No ✅'}`);
    console.log(`Score: ${(moderacion.toxicity_score * 100).toFixed(0)}%`);
  } catch (error) {
    console.error('Error:', error.message);
  }

  // Ejemplo 3: Predicción
  console.log('\n📈 PREDICTION API');
  console.log('-'.repeat(40));
  
  try {
    const fechas = [];
    const valores = [100, 105, 102, 108, 115, 112, 120, 118, 125, 130, 128, 135, 140, 138, 145];
    for (let i = 1; i <= 15; i++) {
      fechas.push(`2024-01-${i.toString().padStart(2, '0')}`);
    }
    
    const prediccion = await client.predecirSerie(fechas, valores, 5);
    console.log(`MAPE: ${(prediccion.mape * 100).toFixed(1)}%`);
    console.log('Predicciones:');
    prediccion.predictions.forEach(p => {
      console.log(`  ${p.date}: ${p.value.toFixed(2)}`);
    });
  } catch (error) {
    console.error('Error:', error.message);
  }

  console.log('\n' + '='.repeat(50));
  console.log('✅ Ejemplos completados');
  console.log('📖 Más info: https://github.com/apisdom/docs');
}

// Descomentar para ejecutar ejemplos:
// ejemplos();
