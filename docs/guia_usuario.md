# Guia de Usuario — FinBot

Agente Financiero con Inteligencia Artificial · EAFIT 2026-1

---

## Que es FinBot?

FinBot es un agente conversacional que responde preguntas financieras en tiempo real usando el patron ReAct (Reason + Act). Consulta precios de acciones, tasas de cambio y noticias del mercado de forma automatica.

---

## Requisitos previos

- Python 3.9 o superior
- Cuenta en Groq (https://console.groq.com) para obtener la API key gratuita
- Conexion a internet

---

## Instalacion paso a paso

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/JoseDanielCU/Final_Project_AI.git
cd Final_Project_AI
```

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3 — Configurar la API key

Crea un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```
GROQ_API_KEY=gsk_tu_api_key_aqui
```

Para obtener tu API key gratuita:
1. Ve a https://console.groq.com
2. Crea una cuenta o inicia sesion
3. En el menu lateral, haz clic en **API Keys**
4. Haz clic en **Create API Key**
5. Copia la key generada y pegala en el archivo `.env`

### Paso 4 — Correr la aplicacion

```bash
python -m streamlit run src/agents/app.py
```

La aplicacion se abre automaticamente en el navegador en `http://localhost:8501`.

---

## Uso de la aplicacion

### Pantalla principal

Al abrir la aplicacion verás:

- **Panel izquierdo (sidebar):** estado de la API, herramientas disponibles y ejemplos de preguntas
- **Area central:** historial de conversacion con FinBot
- **Barra inferior:** campo de texto para escribir tu pregunta y boton Enviar

### Como hacer una consulta

**Opcion 1 — Botones de ejemplo:**
En el sidebar hay 5 preguntas predefinidas. Haz clic en cualquiera para enviarla directamente.

**Opcion 2 — Pregunta propia:**
Escribe tu pregunta en el campo de texto y haz clic en **Enviar**.

### Tipos de preguntas soportadas

| Tipo | Ejemplos |
|------|---------|
| Precio de acciones | "Cuanto vale una accion de Tesla?", "Como esta NVIDIA hoy?" |
| Tasa de cambio | "A cuanto esta el dolar en pesos?", "Cual es la tasa EUR a COP?" |
| Noticias financieras | "Que noticias hay sobre Bitcoin?", "Novedades del mercado petrolero" |
| Consultas combinadas | "Como esta Apple vs Google en bolsa?" |

### Ver el razonamiento del agente

Cada respuesta incluye un panel **"Ver razonamiento ReAct"** que puedes expandir para ver el proceso interno del agente:

- **Thought:** lo que el agente razona antes de actuar
- **Action:** la herramienta que decide usar
- **Observation:** el resultado que devuelve la herramienta
- **Final Answer:** la respuesta elaborada para el usuario

### Limpiar la conversacion

En el sidebar, al final, hay un boton **"Limpiar conversacion"** que reinicia el historial de chat.

---

## Herramientas del agente

### get_stock_price
Consulta el precio actual de una accion en bolsa via Yahoo Finance.

Ejemplos de tickers validos:
- `AAPL` — Apple
- `TSLA` — Tesla
- `GOOGL` — Alphabet (Google)
- `MSFT` — Microsoft
- `NVDA` — NVIDIA
- `AMZN` — Amazon
- `META` — Meta
- `NFLX` — Netflix

### get_exchange_rate
Consulta la tasa de cambio entre dos divisas.

Ejemplos de divisas:
- `USD` — Dolar estadounidense
- `COP` — Peso colombiano
- `EUR` — Euro
- `MXN` — Peso mexicano
- `BRL` — Real brasileno

### get_financial_news
Obtiene titulares recientes de noticias financieras via Yahoo Finance RSS.

Ejemplos de temas:
- Bitcoin, Ethereum
- inflacion, tasas de interes
- petroleo, commodities
- acciones tecnologicas

---

## Preguntas frecuentes

**La app no abre en el navegador**
Abre manualmente `http://localhost:8501` en tu navegador.

**Error: GROQ_API_KEY no configurada**
Verifica que el archivo `.env` existe en la raiz del proyecto y que la key es correcta.

**El agente responde con informacion desactualizada**
Las APIs financieras pueden tener un delay de 15-20 minutos. Los datos son referenciales.

**Error de rate limit en Groq**
La cuenta gratuita tiene un limite diario de tokens. Espera unos minutos o crea una nueva API key.

---

## Estructura del proyecto

```
Final_Project_AI/
├── README.md                        # Documentacion tecnica
├── requirements.txt                 # Dependencias
├── .env.example                     # Template de configuracion
├── docs/
│   ├── informe_final.pdf            # Informe academico
│   └── guia_usuario.md              # Este archivo
├── notebooks/
│   └── 04_llm_rag_agents.ipynb      # Demo del agente
└── src/
    └── agents/
        ├── app.py                   # Interfaz Streamlit
        ├── agent.py                 # Motor ReAct
        └── tools.py                 # Herramientas externas
```

---

## Contacto

- Camilo Andres Melo — cameloa@eafit.edu.co
- Jose Daniel Castaneda — jdcastaneu@eafit.edu.co

Proyecto Final · Inteligencia Artificial · EAFIT 2026-1
