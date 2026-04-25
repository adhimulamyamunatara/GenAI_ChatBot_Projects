import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Gemini Chatbot", page_icon="✨")
st.title("✨Gemini Chatbot")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your GEMINI_API_KEY", type="password")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
if prompt := st.chat_input("Ask anything..."):
    if not api_key:
        st.error("Please set the GEMINI_API_KEY in .env or enter it in the sidebar.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
    except Exception as e:
        st.error(f"Error: {e}")
