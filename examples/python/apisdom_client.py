"""
Apisdom Python Client - Cliente robusto con retry y manejo de errores
Versión: 1.0.0
Documentación: https://github.com/apisdom/docs
"""

import time
from typing import Any

import requests


class ApisdClient:
    """
    Cliente robusto para APIs de Apisdom.
    Maneja: retry, backoff, rate limit, sin créditos.
    
    Ejemplo de uso:
        client = ApisdClient("tu_api_key")
        resultado = client.analizar_sentimiento("¡Excelente producto!")
        print(f"Sentimiento: {resultado['sentiment']} ({resultado['score']:.0%})")
    """
    
    def __init__(self, api_key: str, base_url: str = "https://apisdom.com"):
        """
        Inicializa el cliente.
        
        Args:
            api_key: Tu API Key de apisdom.com/dashboard
            base_url: URL base de la API (no cambiar en producción)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
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
        """
        Analiza el sentimiento de un texto.
        
        Args:
            texto: Texto a analizar (máx 5000 caracteres)
        
        Returns:
            dict con:
            - text: Texto analizado
            - sentiment: 'positive' o 'negative' (modelo binario SST-2)
            - score: Confianza (0.0 a 1.0)
        
        Raises:
            CreditosInsuficientesError: Sin créditos disponibles
            TokenInvalidoError: API Key inválida o revocada
        """
        return self._request_with_retry(
            "POST", 
            "/api/v1/sentiment",
            {"text": texto}
        )
    
    def moderar_contenido(self, texto: str) -> dict:
        """
        Detecta contenido tóxico en un texto.
        
        Args:
            texto: Texto a moderar (máx 5000 caracteres)
        
        Returns:
            dict con:
            - text: Texto analizado
            - is_toxic: True si toxicity_score > 0.7
            - toxicity_score: Puntuación de toxicidad (0.0 a 1.0)
            - categories: Desglose por categorías
        
        Raises:
            CreditosInsuficientesError: Sin créditos disponibles
            TokenInvalidoError: API Key inválida o revocada
        """
        return self._request_with_retry(
            "POST",
            "/api/v1/moderacion", 
            {"text": texto}
        )
    
    def predecir_serie(
        self, 
        dates: list[str], 
        values: list[float], 
        periods: int = 7
    ) -> dict:
        """
        Predice valores futuros de una serie temporal.
        
        Args:
            dates: Lista de fechas en formato 'YYYY-MM-DD' (mín 10)
            values: Lista de valores numéricos (misma longitud que dates)
            periods: Periodos futuros a predecir (1-365, default 7)
        
        Returns:
            dict con:
            - predictions: Lista de {date, value, lower, upper}
            - mape: Error porcentual medio (0.0 a 1.0)
            - quality_warning: Aviso si MAPE > 40%
        
        Raises:
            CreditosInsuficientesError: Sin créditos disponibles
            TokenInvalidoError: API Key inválida o revocada
            ValueError: Si datos no cumplen requisitos
        """
        if len(dates) != len(values):
            raise ValueError("dates y values deben tener la misma longitud")
        if len(dates) < 10:
            raise ValueError("Se necesitan al menos 10 puntos de datos")
        if not 1 <= periods <= 365:
            raise ValueError("periods debe estar entre 1 y 365")
            
        return self._request_with_retry(
            "POST",
            "/api/v1/predictions",
            {"dates": dates, "values": values, "periods": periods}
        )


class CreditosInsuficientesError(Exception):
    """Usuario sin créditos - mostrar mensaje en UI"""
    pass


class TokenInvalidoError(Exception):
    """Token expirado o inválido - redirigir a login"""
    pass


# === EJEMPLO DE USO ===
if __name__ == "__main__":
    # Reemplaza con tu API Key real
    API_KEY = "tu_api_key_aqui"
    
    client = ApisdClient(API_KEY)
    
    # Ejemplo 1: Análisis de sentimiento
    print("=" * 50)
    print("🎭 ANÁLISIS DE SENTIMIENTO")
    print("=" * 50)
    
    try:
        resultado = client.analizar_sentimiento("¡Me encanta este servicio!")
        print(f"Texto: {resultado['text']}")
        print(f"Sentimiento: {resultado['sentiment']}")
        print(f"Confianza: {resultado['score']:.0%}")
        
    except CreditosInsuficientesError:
        print("⚠️ Sin créditos. Recarga en apisdom.com/dashboard")
    except TokenInvalidoError:
        print("🔒 API Key inválida. Obtén una nueva en el Dashboard")
    
    # Ejemplo 2: Moderación de contenido
    print("\n" + "=" * 50)
    print("🛡️ MODERACIÓN DE CONTENIDO")
    print("=" * 50)
    
    try:
        resultado = client.moderar_contenido("Gracias por tu ayuda, eres genial!")
        print(f"Texto: {resultado['text']}")
        print(f"¿Es tóxico?: {'Sí' if resultado['is_toxic'] else 'No'}")
        print(f"Score: {resultado['toxicity_score']:.0%}")
        
    except CreditosInsuficientesError:
        print("⚠️ Sin créditos. Recarga en apisdom.com/dashboard")
    
    # Ejemplo 3: Predicción de series temporales
    print("\n" + "=" * 50)
    print("📈 PREDICCIÓN DE SERIES TEMPORALES")
    print("=" * 50)
    
    try:
        # Datos de ejemplo: 15 días de ventas
        fechas = [f"2024-01-{i:02d}" for i in range(1, 16)]
        valores = [100, 105, 102, 108, 115, 112, 120, 118, 125, 130, 128, 135, 140, 138, 145]
        
        resultado = client.predecir_serie(fechas, valores, periods=5)
        
        print(f"MAPE (error): {resultado['mape']:.1%}")
        print("\nPredicciones:")
        for pred in resultado['predictions']:
            print(f"  {pred['date']}: {pred['value']:.2f}")
        
        if resultado.get('quality_warning'):
            print(f"\n⚠️ Aviso: {resultado['quality_warning']}")
            
    except CreditosInsuficientesError:
        print("⚠️ Sin créditos. Recarga en apisdom.com/dashboard")
    except ValueError as e:
        print(f"❌ Error en datos: {e}")
