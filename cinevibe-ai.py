import os
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CineVibe | AI Agent Platform",
    page_icon="⚡",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. ESTILIZAÇÃO CSS ESTILO RENDER.COM
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    #MainMenu, footer, header, [data-testid="stHeader"] {
        display: none !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #09090b !important;
        background-image: 
            radial-gradient(circle at 85% 20%, rgba(120, 40, 200, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 15% 80%, rgba(0, 229, 153, 0.04) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
        color: #f4f4f5 !important;
    }

    .render-hero {
        text-align: left;
        padding: 35px 0 25px 0;
    }

    .render-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #00e599;
        color: #000000;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 6px 14px;
        border-radius: 4px;
        margin-bottom: 20px;
        letter-spacing: -0.01em;
        box-shadow: 0 0 20px rgba(0, 229, 153, 0.25);
    }

    .render-title {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.04em !important;
        line-height: 1.1 !important;
        margin-bottom: 14px !important;
    }

    .render-subtitle {
        color: #a1a1aa !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        letter-spacing: -0.01em !important;
        max-width: 600px;
    }

    .stChatMessage {
        background-color: #121318 !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
        padding: 18px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }

    .stChatInputContainer > div {
        background-color: #121318 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }

    .stChatInputContainer > div:focus-within {
        border-color: #00e599 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0d0e12 !important;
        border-right: 1px solid #27272a !important;
    }

    .sidebar-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #00e599;
        background: rgba(0, 229, 153, 0.1);
        border: 1px solid rgba(0, 229, 153, 0.2);
        padding: 4px 10px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CABEÇALHO ESTILO RENDER.COM
# -----------------------------------------------------------------------------
st.markdown("""
<div class="render-hero">
    <div class="render-badge">$ cinevibe --agent-start</div>
    <h1 class="render-title">Your fastest path to film recommendations</h1>
    <p class="render-subtitle">Infraestrutura inteligente de curadoria audiovisual alimentada por LLM em tempo real para a nova geração.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. GERENCIAMENTO DE API KEY & SIDEBAR
# -----------------------------------------------------------------------------
api_key = os.environ.get("GROQ_API_KEY", "")

try:
    if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

with st.sidebar:
    st.markdown('<div class="sidebar-status">● DEPLOYED / ACTIVE</div>', unsafe_allow_html=True)
    st.title("⚙️ Control Panel")
    
    if not api_key:
        api_key = st.text_input("GROQ_API_KEY:", type="password", placeholder="gsk_...")
        st.caption("🔑 Obtain your key at console.groq.com")
    
    st.markdown("---")
    st.markdown("### 🛠️ Runtime Tech")
    st.markdown("- **Engine:** Python 3.11")
    st.markdown("- **Model:** Llama-3.3-70b-versatile")
    st.markdown("- **Inference:** Groq LPU™")

if not api_key:
    st.info("👋 Por favor, insira sua chave GROQ_API_KEY na barra lateral para inicializar o agente.")
    st.stop()

client = Groq(api_key=api_key)

# -----------------------------------------------------------------------------
# 5. PERSONA DO AGENTE
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
Você é o 'CineVibe', um crítico de cinema e séries ultra moderno, jovem e imerso na cultura pop (Gen Z/TikTok).
Sua linguagem é empolgada e cheia de gírias atuais (como: "puro suco de", "hitou", "vibe", "entregou tudo", "cinema absoluto", "não ironicamente", "obcecado").

REGRAS:
1. Recomende EXATAMENTE 3 opções parecidas sempre que o usuário mencionar um filme/série.
2. Para cada indicação, faça uma justificativa dinâmica estilo review rápida de TikTok.
3. Use emojis e negrito para organizar a resposta.
"""

# -----------------------------------------------------------------------------
# 6. HISTÓRICO DE CHAT
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "System ready. 🍿✨ Qual foi o último filme ou série que te deixou obcecado? Manda o nome que te entrego 3 recomendações de elite!"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Insira o nome de um filme ou série..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing prompt... 🎬"):
            try:
                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]

                completion = client.chat.completions.create(
                    messages=messages_payload,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=800
                )

                response_text = completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Error connecting to Groq API: {e}")