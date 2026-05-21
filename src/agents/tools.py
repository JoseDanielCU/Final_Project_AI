"""
tools.py - Herramientas del Agente Financiero
Proyecto Final IA - EAFIT 2026-1
"""

import yfinance as yf
import requests
from datetime import datetime


# ─────────────────────────────────────────────
# TOOL 1: Precio de acción en tiempo real
# ─────────────────────────────────────────────
def get_stock_price(ticker: str) -> dict:
    """
    Obtiene el precio actual de una acción usando Yahoo Finance.
    
    Args:
        ticker: Símbolo de la acción (ej: AAPL, GOOGL, AMZN, MSFT, TSLA)
    
    Returns:
        dict con precio actual, cambio porcentual y nombre de la empresa
    """
    try:
        ticker = ticker.upper().strip()
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="2d")

        if hist.empty:
            return {"error": f"No se encontró información para el ticker '{ticker}'."}

        precio_actual = round(hist["Close"].iloc[-1], 2)
        precio_anterior = round(hist["Close"].iloc[-2], 2) if len(hist) > 1 else precio_actual
        cambio_pct = round(((precio_actual - precio_anterior) / precio_anterior) * 100, 2)
        nombre = info.get("longName", ticker)
        moneda = info.get("currency", "USD")

        return {
            "ticker": ticker,
            "nombre": nombre,
            "precio_actual": precio_actual,
            "precio_anterior": precio_anterior,
            "cambio_porcentual": cambio_pct,
            "moneda": moneda,
            "tendencia": "📈 subiendo" if cambio_pct > 0 else "📉 bajando" if cambio_pct < 0 else "➡️ estable"
        }
    except Exception as e:
        return {"error": f"Error al consultar '{ticker}': {str(e)}"}


# ─────────────────────────────────────────────
# TOOL 2: Tasa de cambio de divisas
# ─────────────────────────────────────────────
def get_exchange_rate(base: str = "USD", target: str = "COP") -> dict:
    try:
        base = base.upper().strip()
        target = target.upper().strip()
        
        # API 1: exchangerate-api (gratuita, sin key)
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        tasa = data["rates"].get(target)
        if not tasa:
            return {"error": f"No se encontró la tasa para {base} → {target}"}

        return {
            "base": base,
            "target": target,
            "tasa": round(tasa, 4),
            "fecha": data.get("time_last_update_utc", "hoy"),
            "interpretacion": f"1 {base} = {round(tasa, 2)} {target}"
        }
    except Exception as e:
        return {"error": f"Error al consultar tasa {base}/{target}: {str(e)}"}


# ─────────────────────────────────────────────
# TOOL 3: Resumen de noticias financieras
# ─────────────────────────────────────────────
def get_financial_news(tema: str = "mercados financieros") -> dict:
    """
    Obtiene titulares recientes de noticias financieras usando GNews API (gratuita).
    Fallback: usa RSS de Yahoo Finance si no hay API key configurada.
    
    Args:
        tema: Tema a buscar (ej: "inflación Colombia", "Bitcoin", "petróleo")
    
    Returns:
        dict con lista de titulares y fuentes
    """
    try:
        import feedparser
        # RSS gratuito de Yahoo Finance (no requiere API key)
        query = tema.replace(" ", "+")
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={query}&region=US&lang=en-US"
        feed = feedparser.parse(url)

        if not feed.entries:
            # Fallback: noticias generales de Yahoo Finance
            url = "https://feeds.finance.yahoo.com/rss/2.0/headline?region=US&lang=en-US"
            feed = feedparser.parse(url)

        noticias = []
        for entry in feed.entries[:5]:
            noticias.append({
                "titulo": entry.get("title", "Sin título"),
                "fuente": entry.get("source", {}).get("title", "Yahoo Finance") if hasattr(entry.get("source", ""), "get") else "Yahoo Finance",
                "fecha": entry.get("published", "N/A"),
                "link": entry.get("link", "")
            })

        if not noticias:
            return {"error": "No se encontraron noticias para el tema especificado."}

        return {
            "tema": tema,
            "cantidad": len(noticias),
            "noticias": noticias,
            "fuente_datos": "Yahoo Finance RSS"
        }
    except Exception as e:
        return {"error": f"Error al obtener noticias sobre '{tema}': {str(e)}"}


# ─────────────────────────────────────────────
# Registry de herramientas (usado por el agente)
# ─────────────────────────────────────────────
TOOLS = {
    "get_stock_price": {
        "fn": get_stock_price,
        "description": "Obtiene el precio actual de una acción en bolsa. Input: ticker de la acción (ej: AAPL, GOOGL, TSLA, AMZN, MSFT, NVDA, META, NFLX).",
        "args": ["ticker"]
    },
    "get_exchange_rate": {
        "fn": get_exchange_rate,
        "description": "Obtiene la tasa de cambio entre dos monedas. Input: base (moneda origen, ej: USD) y target (moneda destino, ej: COP, EUR, MXN). Por defecto USD a COP.",
        "args": ["base", "target"]
    },
    "get_financial_news": {
        "fn": get_financial_news,
        "description": "Obtiene titulares recientes de noticias financieras. Input: tema de búsqueda (ej: 'Bitcoin', 'inflación', 'petróleo', 'acciones tecnológicas').",
        "args": ["tema"]
    }
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Ejecuta una herramienta por nombre y retorna el resultado como string."""
    if tool_name not in TOOLS:
        return f"Error: herramienta '{tool_name}' no existe. Herramientas disponibles: {list(TOOLS.keys())}"
    
    try:
        result = TOOLS[tool_name]["fn"](**tool_input)
        return str(result)
    except TypeError as e:
        return f"Error en argumentos de '{tool_name}': {str(e)}"
