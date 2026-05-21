# 📈 FinBot — Agente Financiero con IA

> Proyecto Final · Inteligencia Artificial · EAFIT 2026-1

FinBot es un agente conversacional que usa el patrón **ReAct (Reason + Act)** para responder preguntas financieras en tiempo real. Combina un LLM (Llama 3.3 vía Groq) con herramientas externas para consultar precios de acciones, tasas de cambio y noticias del mercado.

---

## 🚀 Demo rápida

```
Usuario: ¿Cuánto vale una acción de Apple y a cómo está el dólar hoy?

🧠 Thought: Necesito consultar el precio de AAPL y la tasa USD/COP
⚡ Action: get_stock_price | Input: {"ticker": "AAPL"}
🔭 Observation: {"precio_actual": 189.5, "cambio": +1.2%, ...}
⚡ Action: get_exchange_rate | Input: {"base": "USD", "target": "COP"}
🔭 Observation: {"tasa": 4152.3, ...}
✅ Final Answer: Apple (AAPL) cotiza a $189.50 USD (📈 +1.2%). 
   Con el dólar a $4,152 COP, eso equivale a ~$786,814 pesos colombianos por acción.
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/finbot-eafit.git
cd finbot-eafit
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

Obtén tu API key gratis en: [console.groq.com](https://console.groq.com)

### 4. Correr la aplicación
```bash
streamlit run app.py
```

---

## 🛠️ Herramientas del agente

| Herramienta | Descripción | API/Fuente |
|-------------|-------------|------------|
| `get_stock_price` | Precio actual de acciones en bolsa | Yahoo Finance (yfinance) |
| `get_exchange_rate` | Tasa de cambio entre divisas | Frankfurter API (gratuita) |
| `get_financial_news` | Titulares de noticias financieras | Yahoo Finance RSS |

---

## 🏗️ Arquitectura

```
app.py (Streamlit UI)
    └── agent.py (Motor ReAct)
            ├── Groq API (Llama 3.3-70b)
            └── tools.py
                    ├── get_stock_price()   → yfinance
                    ├── get_exchange_rate() → Frankfurter API
                    └── get_financial_news() → Yahoo RSS
```

**Patrón ReAct:**
```
User Query → Thought → Action → Observation → (loop) → Final Answer
```

---

## 📁 Estructura del proyecto

```
finbot-eafit/
├── app.py              # Interfaz Streamlit
├── agent.py            # Lógica del agente ReAct
├── tools.py            # Herramientas externas
├── requirements.txt    # Dependencias
├── .env.example        # Template de configuración
├── .gitignore
└── docs/
    └── informe_final.pdf
```

---

## 📊 Stack tecnológico

- **LLM:** Llama 3.3-70b-versatile via [Groq](https://groq.com)
- **UI:** [Streamlit](https://streamlit.io)
- **Patrón de razonamiento:** ReAct (Reason + Act)
- **APIs:** yfinance · Frankfurter · Yahoo Finance RSS

---

## 👥 Equipo

| Nombre | Contribución |
|--------|-------------|
| [Nombre 1] | Arquitectura del agente, herramientas |
| [Nombre 2] | UI Streamlit, integración, informe |

---

*Proyecto desarrollado para el curso de Inteligencia Artificial · EAFIT 2026-1*
