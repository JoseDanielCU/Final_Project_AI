"""
agent.py - Lógica del Agente ReAct Financiero
Proyecto Final IA - EAFIT 2026-1
"""
 
import os
import re
import json
from groq import Groq
from tools import execute_tool, TOOLS
 
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("No se encontró GROQ_API_KEY.")
    return Groq(api_key=api_key)
 
 
def build_system_prompt() -> str:
    tools_desc = "\n".join([
        f"- {name}: {info['description']}"
        for name, info in TOOLS.items()
    ])
    return f"""Eres FinBot, un agente financiero inteligente.
 
Tienes acceso a estas herramientas:
{tools_desc}
 
INSTRUCCIONES CRÍTICAS - sigue este formato EXACTO sin excepción:
 
Thought: [tu razonamiento]
Action: get_stock_price
Action Input: {{"ticker": "AAPL"}}
 
O para tasa de cambio:
Thought: [tu razonamiento]
Action: get_exchange_rate
Action Input: {{"base": "USD", "target": "COP"}}
 
O para noticias:
Thought: [tu razonamiento]
Action: get_financial_news
Action Input: {{"tema": "bitcoin"}}
 
Después de ver la Observation, da tu respuesta final:
Thought: [análisis del resultado]
Final Answer: [respuesta completa en español con emojis]
 
REGLAS:
1. SIEMPRE usa exactamente un Action antes del Final Answer
2. El Action DEBE ser uno de: get_stock_price, get_exchange_rate, get_financial_news
3. NO inventes datos - usa SOLO lo que devuelve la herramienta
4. Responde en español
"""
 
 
def parse_action(text: str):
    """Extrae Action y Action Input del texto del LLM."""
    action_match = re.search(r'Action:\s*(\w+)', text)
    input_match = re.search(r'Action Input:\s*(\{.*?\})', text, re.DOTALL)
    
    action_name = None
    action_input = {}
    
    if action_match:
        action_name = action_match.group(1).strip()
    
    if input_match:
        try:
            raw = input_match.group(1).strip()
            action_input = json.loads(raw)
        except:
            action_input = {}
    
    return action_name, action_input
 
 
def parse_steps(text: str) -> list:
    """Parsea el texto en pasos visibles para la UI."""
    steps = []
    
    for thought in re.findall(r'Thought:\s*(.+?)(?=Action:|Final Answer:|$)', text, re.DOTALL):
        content = thought.strip()
        if content:
            steps.append({"type": "thought", "content": content})
    
    for action in re.findall(r'Action:\s*(\w+)', text):
        steps.append({"type": "action", "content": action.strip()})
    
    for obs in re.findall(r'Observation:\s*(.+?)(?=Thought:|Final Answer:|$)', text, re.DOTALL):
        content = obs.strip()
        if content:
            steps.append({"type": "observation", "content": content})
    
    final_match = re.search(r'Final Answer:\s*(.+?)$', text, re.DOTALL)
    if final_match:
        steps.append({"type": "final_answer", "content": final_match.group(1).strip()})
    
    return steps
 
 
def run_react_agent(user_query: str, chat_history: list, max_iterations: int = 3) -> dict:
    client = get_groq_client()
    
    messages = [{"role": "system", "content": build_system_prompt()}]
    
    for msg in chat_history[-4:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_query})
    
    full_trace = ""
    all_steps = []
    
    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.1,
            max_tokens=1000,
        )
        
        llm_output = response.choices[0].message.content.strip()
        full_trace += llm_output + "\n"
        
        # Verificar si hay Final Answer
        final_match = re.search(r'Final Answer:\s*(.+?)$', llm_output, re.DOTALL)
        if final_match:
            final_answer = final_match.group(1).strip()
            all_steps.extend(parse_steps(llm_output))
            return {
                "steps": all_steps,
                "final_answer": final_answer,
                "full_trace": full_trace,
                "iterations": iteration + 1
            }
        
        # Buscar Action para ejecutar
        action_name, action_input = parse_action(llm_output)
        
        if action_name and action_name in TOOLS:
            observation = execute_tool(action_name, action_input)
            
            # Agregar pasos parciales
            all_steps.extend(parse_steps(llm_output))
            all_steps.append({"type": "observation", "content": str(observation)})
            
            # Continuar con la observación
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({
                "role": "user", 
                "content": f"Observation: {observation}\n\nAhora escribe tu Final Answer basándote en esta información."
            })
        else:
            # No hay acción válida, pedir que responda directamente
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({
                "role": "user",
                "content": "Usa una de las herramientas disponibles: get_stock_price, get_exchange_rate, o get_financial_news. Luego da tu Final Answer."
            })
    
    # Fallback si se agotaron iteraciones
    fallback = "Lo siento, no pude completar el análisis. Por favor intenta de nuevo."
    all_steps.append({"type": "final_answer", "content": fallback})
    
    return {
        "steps": all_steps,
        "final_answer": fallback,
        "full_trace": full_trace,
        "iterations": max_iterations
    }
 