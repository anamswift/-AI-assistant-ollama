import streamlit as st
import requests
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Anam T. — AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Full CSS + Animations ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Quicksand:wght@400;500;600;700&display=swap');

:root {
    --sky:      #e8f4fd;
    --blue:     #2196f3;
    --navy:     #1a237e;
    --gold:     #f9a825;
    --gold2:    #ffcc02;
    --white:    #ffffff;
    --text:     #1a237e;
    --muted:    #7986cb;
    --radius:   18px;
}

html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif !important;
    background: linear-gradient(160deg, #e8f4fd 0%, #d0eaf8 50%, #e8eaf6 100%) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1.5rem 4rem; max-width: 1100px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a237e 0%, #283593 60%, #3949ab 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Quicksand', sans-serif !important;
    color: #ffffff !important;
}

/* ── Welcome Banner ── */
.welcome-wrap {
    position: relative;
    width: 100%;
    min-height: 320px;
    background: linear-gradient(135deg, #1a237e 0%, #1565c0 40%, #0288d1 100%);
    border-radius: 24px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 60px rgba(26,35,126,0.3);
}

.welcome-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 80% 40% at 50% 0%, rgba(255,255,255,0.15) 0%, transparent 70%);
}

/* ── Clouds ── */
.cloud {
    position: absolute;
    font-size: 3.5rem;
    animation: cloudDrift linear infinite;
    opacity: 0.55;
}
.cloud:nth-child(1) { top: 8%;  left: -12%; animation-duration:18s; animation-delay:0s;  font-size:4rem; }
.cloud:nth-child(2) { top: 22%; left: -12%; animation-duration:25s; animation-delay:7s;  font-size:2.8rem; }
.cloud:nth-child(3) { top: 5%;  left: -12%; animation-duration:21s; animation-delay:13s; font-size:3.2rem; }

@keyframes cloudDrift {
    0%   { transform: translateX(0); }
    100% { transform: translateX(115vw); }
}

/* ── Floating icons ── */
.floaters { position:absolute; inset:0; pointer-events:none; overflow:hidden; }
.floater  { position:absolute; animation:floatUp linear infinite; opacity:0; }

.floater:nth-child(1)  { left:4%;  font-size:2rem;   animation-duration:7s;  animation-delay:0s;   top:110%; }
.floater:nth-child(2)  { left:13%; font-size:1.6rem;  animation-duration:9s;  animation-delay:1.2s; top:110%; }
.floater:nth-child(3)  { left:23%; font-size:2.5rem;  animation-duration:6s;  animation-delay:2s;   top:110%; }
.floater:nth-child(4)  { left:34%; font-size:1.8rem;  animation-duration:8s;  animation-delay:0.6s; top:110%; }
.floater:nth-child(5)  { left:46%; font-size:2.2rem;  animation-duration:10s; animation-delay:3s;   top:110%; }
.floater:nth-child(6)  { left:57%; font-size:1.5rem;  animation-duration:7s;  animation-delay:1.8s; top:110%; }
.floater:nth-child(7)  { left:67%; font-size:2.4rem;  animation-duration:9s;  animation-delay:4s;   top:110%; }
.floater:nth-child(8)  { left:77%; font-size:1.9rem;  animation-duration:6s;  animation-delay:2.4s; top:110%; }
.floater:nth-child(9)  { left:87%; font-size:2rem;    animation-duration:8s;  animation-delay:0.9s; top:110%; }
.floater:nth-child(10) { left:94%; font-size:1.7rem;  animation-duration:7s;  animation-delay:3.6s; top:110%; }

@keyframes floatUp {
    0%   { transform:translateY(0) rotate(0deg);    opacity:0; }
    8%   { opacity:0.9; }
    90%  { opacity:0.7; }
    100% { transform:translateY(-400px) rotate(12deg); opacity:0; }
}

/* ── Welcome text ── */
.welcome-content {
    position:relative; z-index:10;
    text-align:center; padding:2rem;
    animation:fadeDown 0.9s ease both;
}
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-18px); }
    to   { opacity:1; transform:translateY(0); }
}

.welcome-badge {
    display:inline-block;
    background:rgba(255,255,255,0.15);
    border:1px solid rgba(255,255,255,0.3);
    border-radius:999px;
    padding:5px 18px;
    font-size:0.76rem; font-weight:700;
    letter-spacing:0.14em; text-transform:uppercase;
    color:#c5cae9; margin-bottom:0.9rem;
}
.welcome-name {
    font-family:'Playfair Display', serif;
    font-size:3rem; font-weight:900;
    color:#ffffff; line-height:1.1; margin:0;
    text-shadow:0 4px 20px rgba(0,0,0,0.3);
}
.welcome-name span {
    background:linear-gradient(135deg,#f9a825,#ffcc02);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.welcome-tagline {
    font-size:1rem; color:#c5cae9;
    margin-top:0.5rem; font-weight:500;
}
.welcome-powered {
    margin-top:1.1rem;
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(255,255,255,0.1);
    border:1px solid rgba(255,255,255,0.2);
    border-radius:999px; padding:5px 16px;
    font-size:0.78rem; color:#e8eaf6; font-weight:600;
}

/* ── Sidebar labels ── */
.sidebar-logo {
    font-family:'Playfair Display',serif;
    font-size:1.3rem; font-weight:900;
    color:#ffffff !important; text-align:center;
    padding:1rem 0 0.2rem;
}
.sidebar-sub {
    font-size:0.7rem; color:#9fa8da !important;
    text-align:center; letter-spacing:0.1em;
    text-transform:uppercase; margin-bottom:0.8rem;
}
.sidebar-divider {
    height:1px;
    background:linear-gradient(to right,transparent,rgba(255,255,255,0.2),transparent);
    margin:0.7rem 0;
}
.sidebar-section {
    font-size:0.68rem; font-weight:700;
    letter-spacing:0.13em; text-transform:uppercase;
    color:#9fa8da !important; margin:0.9rem 0 0.25rem;
}
.pill { display:inline-flex; align-items:center; gap:6px; padding:4px 13px; border-radius:999px; font-size:0.7rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; border:1px solid; }
.pill-on  { color:#69f0ae; border-color:#69f0ae; background:rgba(105,240,174,0.12); }
.pill-off { color:#ff5252; border-color:#ff5252; background:rgba(255,82,82,0.12); }

/* ── Chat ── */
.chat-outer {
    max-height:50vh; overflow-y:auto;
    padding:0.5rem 0.5rem 1rem;
    scrollbar-width:thin; scrollbar-color:#c5cae9 transparent;
}
.chat-outer::-webkit-scrollbar { width:4px; }
.chat-outer::-webkit-scrollbar-thumb { background:#c5cae9; border-radius:4px; }

.msg-row { display:flex; align-items:flex-end; gap:10px; margin-bottom:0.9rem; animation:popIn 0.3s cubic-bezier(0.34,1.56,0.64,1) both; }
.msg-row.user { flex-direction:row-reverse; }

@keyframes popIn {
    from { opacity:0; transform:scale(0.85) translateY(8px); }
    to   { opacity:1; transform:scale(1)    translateY(0); }
}

.avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; flex-shrink:0; box-shadow:0 4px 12px rgba(0,0,0,0.15); }
.avatar.user { background:linear-gradient(135deg,#1a237e,#3949ab); }
.avatar.ai   { background:linear-gradient(135deg,#f9a825,#ffcc02); }

.bubble { max-width:68%; padding:0.75rem 1.1rem; border-radius:18px; font-size:0.92rem; line-height:1.6; white-space:pre-wrap; word-break:break-word; box-shadow:0 4px 16px rgba(0,0,0,0.08); }
.bubble.user { background:linear-gradient(135deg,#1a237e,#283593); color:#fff; border-bottom-right-radius:4px; }
.bubble.ai   { background:#fff; color:#1a237e; border-bottom-left-radius:4px; border:1px solid #e3e8f5; }

.meta { font-size:0.62rem; color:#9fa8da; margin-top:3px; padding:0 4px; }
.meta.user { text-align:right; }

.thinking { display:flex; gap:5px; align-items:center; padding:0.65rem 1rem; background:#fff; border:1px solid #e3e8f5; border-radius:18px; border-bottom-left-radius:4px; width:fit-content; box-shadow:0 4px 16px rgba(0,0,0,0.06); }
.dot { width:8px; height:8px; border-radius:50%; animation:boing 1.2s infinite ease-in-out; }
.dot:nth-child(1) { background:#1a237e; }
.dot:nth-child(2) { background:#f9a825; animation-delay:0.2s; }
.dot:nth-child(3) { background:#0288d1; animation-delay:0.4s; }
@keyframes boing {
    0%,80%,100% { transform:scale(0.5); opacity:0.4; }
    40%          { transform:scale(1.2); opacity:1; }
}

/* ── Input ── */
.stTextArea textarea {
    background:#fff !important; border:2px solid #c5cae9 !important;
    border-radius:14px !important; color:#1a237e !important;
    font-family:'Quicksand',sans-serif !important; font-size:0.92rem !important;
    font-weight:500 !important; resize:none;
    box-shadow:0 4px 16px rgba(26,35,126,0.08) !important;
}
.stTextArea textarea:focus { border-color:#1a237e !important; box-shadow:0 4px 20px rgba(26,35,126,0.18) !important; }
.stTextArea textarea::placeholder { color:#9fa8da !important; }

.stButton > button {
    background:linear-gradient(135deg,#f9a825,#ffcc02) !important;
    color:#1a237e !important; border:none !important; border-radius:12px !important;
    font-family:'Quicksand',sans-serif !important; font-weight:700 !important;
    font-size:0.88rem !important; padding:0.55rem 1.2rem !important;
    box-shadow:0 4px 16px rgba(249,168,37,0.35) !important;
    transition:transform 0.15s,box-shadow 0.15s !important; width:100% !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 24px rgba(249,168,37,0.45) !important; }

.stSelectbox > div > div { background:rgba(255,255,255,0.15) !important; border-color:rgba(255,255,255,0.2) !important; color:#fff !important; border-radius:10px !important; }

.char-count { font-size:0.68rem; color:#9fa8da; text-align:right; margin-top:-0.4rem; }
.empty-state { text-align:center; padding:2.5rem 1rem; color:#9fa8da; font-size:0.9rem; }
.empty-state .big { font-size:2.5rem; margin-bottom:0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
OLLAMA_BASE = "http://localhost:11434"

def get_models():
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return []

def check_ollama():
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def chat_with_ollama(model, messages, temperature, max_tokens):
    payload = {
        "model": model, "messages": messages, "stream": True,
        "options": {"temperature": temperature, "num_predict": max_tokens}
    }
    try:
        with requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    done  = chunk.get("done", False)
                    yield token, done
    except requests.exceptions.ConnectionError:
        yield "⚠️ Cannot connect to Ollama. Run `ollama serve` first!", True
    except Exception as e:
        yield f"⚠️ Error: {str(e)}", True

# ── Session state ─────────────────────────────────────────────────────────────
if "history"  not in st.session_state: st.session_state.history  = []
if "thinking" not in st.session_state: st.session_state.thinking = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-logo">🎓 Anam T.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-sub">AI Learning Assistant</p>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    online = check_ollama()
    st.markdown(
        '<span class="pill pill-on">⬤ &nbsp;Ollama online</span>' if online
        else '<span class="pill pill-off">⬤ &nbsp;Ollama offline</span>',
        unsafe_allow_html=True
    )
    if not online:
        st.caption("Run `ollama serve` to start.")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section">🤖 Model</p>', unsafe_allow_html=True)

    models = get_models()
    if models:
        model = st.selectbox("", models, label_visibility="collapsed")
    else:
        st.warning("No models found!\nRun: `ollama pull tinyllama`")
        model = st.text_input("Model name", value="tinyllama", label_visibility="collapsed")

    st.markdown('<p class="sidebar-section">⚙️ Settings</p>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05, help="Higher = more creative")
    max_tokens  = st.slider("Max tokens", 64, 2048, 512, 64)

    st.markdown('<p class="sidebar-section">💬 Personality</p>', unsafe_allow_html=True)
    system_prompt = st.text_area("", value="You are Anam T., a friendly, warm and helpful AI assistant. Be encouraging, clear and concise in your answers.", height=90, label_visibility="collapsed")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    n_turns = len([m for m in st.session_state.history if m["role"] == "user"])
    st.markdown(f'<p class="sidebar-section">📊 {n_turns} message{"s" if n_turns!=1 else ""} sent</p>', unsafe_allow_html=True)

    if st.button("🗑️  Clear Chat", key="reset"):
        st.session_state.history  = []
        st.rerun()

# ── Welcome Banner ────────────────────────────────────────────────────────────
st.markdown("""
<div class="welcome-wrap">
    <div class="cloud">☁️</div>
    <div class="cloud">⛅</div>
    <div class="cloud">☁️</div>
    <div class="floaters">
        <div class="floater">📚</div>
        <div class="floater">✏️</div>
        <div class="floater">🎓</div>
        <div class="floater">📖</div>
        <div class="floater">☁️</div>
        <div class="floater">🖊️</div>
        <div class="floater">📚</div>
        <div class="floater">🎓</div>
        <div class="floater">✏️</div>
        <div class="floater">⭐</div>
    </div>
    <div class="welcome-content">
        <div class="welcome-badge">🎓 &nbsp; Welcome to your AI Assistant</div>
        <p class="welcome-name">Hi, I'm <span>Anam T.</span></p>
        <p class="welcome-tagline">📚 Your personal learning companion — ask me anything!</p>
        <div class="welcome-powered">🤖 &nbsp; Powered by Ollama &nbsp;·&nbsp; 100% Private &nbsp;·&nbsp; Runs on your PC</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chat window ───────────────────────────────────────────────────────────────
chat_placeholder = st.empty()

def render_chat():
    if not st.session_state.history:
        chat_placeholder.markdown("""
        <div class="empty-state">
            <div class="big">💬</div>
            <p>Start chatting with <strong>Anam T.</strong> below!<br>
            She's ready to help you learn anything. 🌟</p>
        </div>""", unsafe_allow_html=True)
        return

    html = '<div class="chat-outer"><div>'
    for m in st.session_state.history:
        role  = m["role"]
        text  = m["content"]
        ts    = m.get("ts", "")
        emoji = "👤" if role == "user" else "🎓"
        cls   = role if role == "user" else "ai"
        html += f"""
        <div class="msg-row {cls}">
            <div class="avatar {cls}">{emoji}</div>
            <div>
                <div class="bubble {cls}">{text}</div>
                <div class="meta {cls}">{ts}</div>
            </div>
        </div>"""
    html += "</div></div>"
    chat_placeholder.markdown(html, unsafe_allow_html=True)

render_chat()

# ── Input bar ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_area(
        "Message", placeholder="Ask Anam T. anything… 📝",
        height=80, label_visibility="collapsed",
        key="user_input", disabled=st.session_state.thinking,
    )
    st.markdown(f'<p class="char-count">{len(user_input) if user_input else 0} chars</p>', unsafe_allow_html=True)

with col_btn:
    st.write("")
    send = st.button("Send ✈️", disabled=st.session_state.thinking or not (user_input or "").strip())

# ── Send logic ────────────────────────────────────────────────────────────────
if send and (user_input or "").strip() and not st.session_state.thinking:
    ts_now = datetime.now().strftime("%H:%M")
    st.session_state.history.append({"role": "user", "content": user_input.strip(), "ts": ts_now})

    ollama_msgs = [{"role": "system", "content": system_prompt}]
    for m in st.session_state.history:
        ollama_msgs.append({"role": m["role"], "content": m["content"]})

    st.session_state.thinking = True
    render_chat()

    think_ph = st.empty()
    think_ph.markdown("""
    <div class="msg-row ai">
        <div class="avatar ai">🎓</div>
        <div class="thinking">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    response_text = ""
    stream_ph = st.empty()

    for token, done in chat_with_ollama(model, ollama_msgs, temperature, max_tokens):
        response_text += token
        stream_ph.markdown(f"""
        <div class="msg-row ai">
            <div class="avatar ai">🎓</div>
            <div><div class="bubble ai">{response_text}▌</div></div>
        </div>""", unsafe_allow_html=True)
        if done:
            break

    think_ph.empty()
    stream_ph.empty()

    st.session_state.history.append({
        "role": "assistant", "content": response_text,
        "ts": datetime.now().strftime("%H:%M"),
    })
    st.session_state.thinking = False
    st.rerun()
