import streamlit as st
from groq import Groq
import os
import json
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Groq Chatbot", page_icon="🐈‍⬛", layout="wide")

# --- CSS STYLING (Reference Image Alignment) ---
st.markdown("""
<style>
    /* Main Backgrounds */
    .stApp { background: #171717; color: #ececec; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #2f2f2f; width: 260px !important; }
    
    /* Text Colors */
    [data-testid="stSidebar"] *, .stMarkdown, p, span, div, h1, h2, h3 { color: #ececec !important; }
    
    /* Sidebar Specific */
    .sidebar-title { font-size: 20px; font-weight: 600; padding: 16px; display: flex; align-items: center; gap: 10px; }
    .history-label { font-size: 12px; color: #666 !important; margin: 20px 0 10px 12px; font-weight: 600; }
    
    /* Google Button with Colorful G SVG */
    .google-auth-container { padding: 0 12px 10px 12px; }
    .google-btn-styled {
        display: flex; align-items: center; justify-content: flex-start;
        gap: 12px; background: transparent; border: 1px solid #444;
        border-radius: 8px; padding: 10px 16px; cursor: pointer; transition: 0.2s;
        width: 100%; color: #ececec; font-size: 14px; font-weight: 500;
    }
    .google-btn-styled:hover { background: #2f2f2f; border-color: #666; }
    .g-svg { width: 20px; height: 20px; }
    
    /* New Chat Button */
    .new-chat-container { padding: 0 12px 10px 12px; }
    .stButton button { border-radius: 8px !important; background: transparent !important; border: 1px solid #444 !important; }
    .stButton button:hover { background: #2f2f2f !important; }
    
    /* Sidebar Footer */
    .sidebar-footer { padding: 10px 12px; border-top: 1px solid #2f2f2f; margin-top: auto; }
    
    /* Main Panel */
    .chat-heading { font-size: 32px; font-weight: 500; text-align: center; margin-top: 15vh; color: #ececec; }
    
    /* Chat Messages - Dark Pills for User with Emojis */
    .chat-msg-container { display: flex; align-items: flex-start; margin-bottom: 20px; gap: 10px; }
    .chat-msg-container.user { flex-direction: row-reverse; margin-left: auto; margin-right: 15%; }
    .chat-msg-container.assistant { margin-left: 15%; }
    .chat-emoji { font-size: 24px; flex-shrink: 0; margin-top: 5px; }
    .chat-msg { padding: 12px 20px; border-radius: 20px; line-height: 1.5; font-size: 15px; width: fit-content; max-width: 600px; }
    .chat-user { background: #2f2f2f; color: #fff !important; }
    .chat-assistant { background: transparent; }
    
    /* WhatsApp Style Chat Input */
    [data-testid="stChatInput"] { 
        background: #2f2f2f !important; 
        border-radius: 30px !important; 
        border: 1px solid #3d3d3d !important; 
        max-width: 800px; 
        margin: 0 auto !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }
    [data-testid="stChatInput"] textarea { 
        background: transparent !important; 
        color: #ececec !important; 
        padding: 12px 20px !important;
        font-size: 15px !important;
    }
    [data-testid="stChatInput"] button { 
        background: #00a884 !important; 
        border-radius: 50% !important; 
        padding: 8px !important;
    }

    /* Hide Default Streamlit Branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "sessions" not in st.session_state:
    try:
        with open("chat_history.json", "r") as f: st.session_state.sessions = json.load(f)
    except: st.session_state.sessions = {}
if "chat_id" not in st.session_state: st.session_state.chat_id = None
if "show_menu" not in st.session_state: st.session_state.show_menu = False
if "authenticated" not in st.session_state: st.session_state.authenticated = False

# --- UTILS ---
def save():
    with open("chat_history.json", "w") as f: json.dump(st.session_state.sessions, f)

def new_chat():
    cid = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    st.session_state.chat_id = cid
    st.session_state.messages = []
    st.session_state.sessions[cid] = {"title": "New Chat", "msgs": []}
    save()
    st.rerun()

def load_chat(cid):
    st.session_state.chat_id = cid
    st.session_state.messages = st.session_state.sessions[cid]["msgs"]
    st.rerun()

def clear_history():
    st.session_state.sessions = {}
    st.session_state.chat_id = None
    st.session_state.messages = []
    if os.path.exists("chat_history.json"): os.remove("chat_history.json")
    st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🐈‍⬛ Groq Chatbot</div>', unsafe_allow_html=True)
    
    # Auth Section with Colorful G SVG
    if not st.session_state.authenticated:
        st.markdown('<div class="google-auth-container">', unsafe_allow_html=True)
        if st.button("🔐 Sign in with Google", use_container_width=True):
            st.session_state.authenticated = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="google-auth-container">**Welcome, User!**</div>', unsafe_allow_html=True)
        if st.button("Sign Out"):
            st.session_state.authenticated = False
            st.rerun()
    
    # New Chat
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("+ New chat", use_container_width=True): new_chat()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="history-label">HISTORY</div>', unsafe_allow_html=True)
    if not st.session_state.sessions:
        st.markdown('<div style="padding-left:12px; color:#666; font-size:13px;">No recent chats</div>', unsafe_allow_html=True)
    for cid, data in list(st.session_state.sessions.items())[::-1][:10]:
        if st.button(f"💬 {data['title'][:20]}", key=f"btn_{cid}", use_container_width=True): load_chat(cid)
    
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    # Sidebar Footer
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    if st.button("🗑️ Clear History", use_container_width=True): clear_history()
    if st.button("🌙 Toggle Theme", use_container_width=True): pass
    st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN UI ---
if not st.session_state.messages:
    st.markdown('<div class="chat-heading">How can I assist you?</div>', unsafe_allow_html=True)
else:
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "assistant"
        emoji = "👤" if role == "user" else "🐈‍⬛"
        bubble_class = "chat-user" if role == "user" else "chat-assistant"
        container_class = "user" if role == "user" else "assistant"
        st.markdown(f'<div class="chat-msg-container {container_class}"><div class="chat-emoji">{emoji}</div><div class="chat-msg {bubble_class}">{m["content"]}</div></div>', unsafe_allow_html=True)

# --- CHAT INPUT ---
prompt = st.chat_input("Type a message")

if prompt:
    if not st.session_state.chat_id:
        cid = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        st.session_state.chat_id = cid
        st.session_state.sessions[cid] = {"title": prompt[:30], "msgs": []}
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.sessions[st.session_state.chat_id]["msgs"] = st.session_state.messages
    save()
    with st.spinner("Thinking..."):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=2048
            )
            ai_msg = resp.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
            st.session_state.sessions[st.session_state.chat_id]["msgs"] = st.session_state.messages
            save()
            st.rerun()
        except Exception as e:
            st.error(f"Error with Groq: {e}")
