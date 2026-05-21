"""
app.py - Interfaz Streamlit del Agente Financiero ReAct
Proyecto Final IA - EAFIT 2026-1
"""
 
import streamlit as st
from dotenv import load_dotenv
import os
 
load_dotenv()
 
# ─────────────────────────────────────────────
# Configuración de la página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinBot — Agente Financiero IA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─────────────────────────────────────────────
# CSS personalizado
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        text-align: center;
        padding: 1rem 0 0.2rem 0;
        letter-spacing: 2px;
    }
    .main-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        font-family: monospace;
    }
    .chat-user {
        background: linear-gradient(135deg, #1f6feb, #388bfd);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(31, 111, 235, 0.3);
    }
    .chat-agent {
        background: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .react-step {
        padding: 8px 12px;
        border-radius: 8px;
        margin: 4px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        border-left: 3px solid;
    }
    .react-thought  { background: #1c2128; border-color: #d29922; color: #e3b341; }
    .react-action   { background: #1c2128; border-color: #3fb950; color: #56d364; }
    .react-observation { background: #1c2128; border-color: #58a6ff; color: #79c0ff; }
    .react-final    { background: #1c2128; border-color: #bc8cff; color: #d2a8ff; }
    .stTextInput > div > div > input {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        border-radius: 10px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="metric-container"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px;
    }
    hr { border-color: #30363d; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# Inicializar estado de sesión
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []
 
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
 
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
 
if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""
 
# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 FinBot")
    st.markdown("*Agente Financiero con IA*")
    st.markdown("---")
 
    api_key = os.environ.get("GROQ_API_KEY", "")
    if api_key:
        st.success("✅ Groq API conectada")
    else:
        st.error("❌ GROQ_API_KEY no configurada")
        st.code("export GROQ_API_KEY='gsk_...'", language="bash")
 
    st.markdown("---")
    st.markdown("### 🛠️ Herramientas disponibles")
    st.markdown("""
    - 📈 **get_stock_price** — Precios de acciones en tiempo real
    - 💱 **get_exchange_rate** — Tasas de cambio (USD, COP, EUR...)
    - 📰 **get_financial_news** — Noticias financieras recientes
    """)
 
    st.markdown("---")
    st.markdown("### 💡 Ejemplos de preguntas")
 
    example_queries = [
        "¿Cuánto vale una acción de Tesla?",
        "¿A cuánto está el dólar en pesos colombianos?",
        "¿Qué noticias hay sobre Bitcoin?",
        "¿Cómo está Apple vs Google en bolsa?",
        "Analiza NVIDIA para invertir",
    ]
 
    for eq in example_queries:
        if st.button(eq, key=f"ex_{eq}", use_container_width=True):
            st.session_state.pending_query = eq
            st.rerun()
 
    st.markdown("---")
    st.markdown(f"**Consultas realizadas:** {st.session_state.query_count}")
 
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.display_messages = []
        st.session_state.query_count = 0
        st.session_state.last_query = ""
        st.session_state.pending_query = ""
        st.rerun()
 
    st.markdown("---")
    st.markdown("*EAFIT 2026-1 · IA Proyecto Final*")
 
# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">📈 FINBOT</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Agente de Análisis Financiero · ReAct Pattern · Powered by Groq + Llama 3.1</div>', unsafe_allow_html=True)
st.markdown("---")
 
# ─────────────────────────────────────────────
# Renderizar pasos ReAct
# ─────────────────────────────────────────────
def render_react_steps(steps: list):
    icons = {
        "thought": "🧠", "action": "⚡",
        "action_input": "📥", "observation": "🔭", "final_answer": "✅"
    }
    css_classes = {
        "thought": "react-thought", "action": "react-action",
        "action_input": "react-action", "observation": "react-observation",
        "final_answer": "react-final"
    }
    labels = {
        "thought": "Thought", "action": "Action",
        "action_input": "Action Input", "observation": "Observation",
        "final_answer": "Final Answer"
    }
    for step in steps:
        stype = step.get("type", "thought")
        if stype == "final_answer":
            continue
        icon = icons.get(stype, "•")
        css = css_classes.get(stype, "react-thought")
        label = labels.get(stype, stype.title())
        content = step.get("content", "")
        st.markdown(
            f'<div class="react-step {css}"><b>{icon} {label}:</b> {content}</div>',
            unsafe_allow_html=True
        )
 
# ─────────────────────────────────────────────
# Área de chat
# ─────────────────────────────────────────────
chat_container = st.container()
 
with chat_container:
    if not st.session_state.display_messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #8b949e;">
            <div style="font-size: 3rem;">📊</div>
            <div style="font-size: 1.1rem; margin-top: 1rem;">
                ¡Hola! Soy <b style="color: #58a6ff;">FinBot</b>, tu agente financiero inteligente.
            </div>
            <div style="margin-top: 0.5rem;">
                Pregúntame sobre precios de acciones, tasas de cambio o noticias del mercado.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    for msg in st.session_state.display_messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">👤 {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            if msg.get("steps"):
                with st.expander("🔍 Ver razonamiento ReAct", expanded=False):
                    render_react_steps(msg["steps"])
            st.markdown(
                f'<div class="chat-agent">🤖 <b>FinBot:</b> {msg["content"]}</div>',
                unsafe_allow_html=True
            )
 
# ─────────────────────────────────────────────
# Input del usuario
# ─────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([5, 1])
 
with col1:
    input_value = st.session_state.pending_query if st.session_state.pending_query else ""
    user_input = st.text_input(
        "Tu pregunta",
        placeholder="Ej: ¿Cuánto vale una acción de Apple? ¿A cómo está el dólar?",
        label_visibility="collapsed",
        key="user_input_field",
        value=input_value
    )
 
with col2:
    send_button = st.button("Enviar 🚀", use_container_width=True)
 
# ─────────────────────────────────────────────
# Determinar query a procesar
# ─────────────────────────────────────────────
query_to_process = None
 
# Caso 1: botón de ejemplo fue presionado
if st.session_state.pending_query and st.session_state.pending_query != st.session_state.last_query:
    query_to_process = st.session_state.pending_query
    st.session_state.pending_query = ""
 
# Caso 2: botón enviar presionado
elif send_button and user_input.strip() and user_input.strip() != st.session_state.last_query:
    query_to_process = user_input.strip()
 
# ─────────────────────────────────────────────
# Procesar la consulta
# ─────────────────────────────────────────────
if query_to_process:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("❌ Configura tu GROQ_API_KEY antes de continuar.")
        st.stop()
 
    st.session_state.last_query = query_to_process
 
    st.session_state.display_messages.append({
        "role": "user",
        "content": query_to_process
    })
 
    with st.spinner("🤔 FinBot está analizando..."):
        try:
            from agent import run_react_agent
 
            result = run_react_agent(
                user_query=query_to_process,
                chat_history=st.session_state.chat_history
            )
 
            final_answer = result["final_answer"]
            steps = result["steps"]
 
            st.session_state.chat_history.append({"role": "user", "content": query_to_process})
            st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
 
            st.session_state.display_messages.append({
                "role": "assistant",
                "content": final_answer,
                "steps": steps
            })
 
            st.session_state.query_count += 1
 
        except Exception as e:
            st.session_state.display_messages.append({
                "role": "assistant",
                "content": f"⚠️ Error: {str(e)}",
                "steps": []
            })
 
    st.rerun()