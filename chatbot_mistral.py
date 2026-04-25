import streamlit as st
from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

st.set_page_config(page_title="Mistral Chatbot", page_icon="🤖")
st.title("🤖Mistral Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask anything..."):
    if not api_key:
        st.error("Please set the MISTRAL_API_KEY in .env or enter it in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = Mistral(api_key=api_key)

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=st.session_state.messages,
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except Exception as e:
        st.error(f"Error: {e}")