# FinBot — Agente Financiero con IA

Proyecto Final · Inteligencia Artificial · EAFIT 2026-1

FinBot es un agente conversacional que usa el patron **ReAct (Reason + Act)** para responder preguntas financieras en tiempo real. Combina un LLM (Llama 3.1 via Groq) con herramientas externas para consultar precios de acciones, tasas de cambio y noticias del mercado.

---

## Demo rapida

```
Usuario: Cuanto vale una accion de Apple y a como esta el dolar hoy?

Thought: Necesito consultar el precio de AAPL y la tasa USD/COP
Action: get_stock_price | Input: {"ticker": "AAPL"}
Observation: {"precio_actual": 189.5, "cambio": +1.2%, ...}
Action: get_exchange_rate | Input: {"base": "USD", "target": "COP"}
Observation: {"tasa": 4152.3, ...}
Final Answer: Apple (AAPL) cotiza a $189.50 USD (+1.2%).
   Con el dolar a $4,152 COP, eso equivale a ~$786,814 pesos colombianos por accion.
```

---

## Instalacion

### 1. Clonar el repositorio
```bash
git clone https://github.com/JoseDanielCU/Final_Project_AI.git
cd Final_Project_AI
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar API key
```bash
cp .env.example .env
# Edita .env y agrega tu GROQ_API_KEY
```

Obtén tu API key gratis en: https://console.groq.com

### 4. Correr la aplicacion
```bash
python -m streamlit run src/agents/app.py
```

---

## Herramientas del agente

| Herramienta | Descripcion | Fuente |
|-------------|-------------|--------|
| `get_stock_price` | Precio actual de acciones en bolsa | Yahoo Finance (yfinance) |
| `get_exchange_rate` | Tasa de cambio entre divisas | Open Exchange Rates API |
| `get_financial_news` | Titulares de noticias financieras | Yahoo Finance RSS |

---

## Arquitectura

```
src/agents/app.py  (Streamlit UI)
    └── agent.py   (Motor ReAct)
            ├── Groq API (Llama 3.1-8b-instant)
            └── tools.py
                    ├── get_stock_price()    -> yfinance
                    ├── get_exchange_rate()  -> Open Exchange Rates
                    └── get_financial_news() -> Yahoo RSS
```

Patron ReAct:
```
User Query -> Thought -> Action -> Observation -> (loop) -> Final Answer
```

---

## Estructura del proyecto

```
Final_Project_AI/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
│   └── informe_final.pdf
├── notebooks/
│   └── 04_llm_rag_agents.ipynb
├── src/
│   └── agents/
│       ├── app.py
│       ├── agent.py
│       └── tools.py
└── data/
    ├── raw/
    └── processed/
```

---

## Stack tecnologico

- LLM: Llama 3.1-8b-instant via Groq (https://groq.com)
- UI: Streamlit (https://streamlit.io)
- Patron de razonamiento: ReAct (Reason + Act)
- APIs: yfinance · Open Exchange Rates · Yahoo Finance RSS

---

## Video demo

Link: (pendiente)

---

## Equipo

| Nombre | Correo | Contribucion |
|--------|--------|-------------|
| Nombre 1 | correo1@eafit.edu.co | Arquitectura del agente, herramientas |
| Nombre 2 | correo2@eafit.edu.co | UI Streamlit, integracion, informe |

---

Proyecto desarrollado para el curso de Inteligencia Artificial · EAFIT 2026-1
