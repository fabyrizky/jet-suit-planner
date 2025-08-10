import streamlit as st
import os
import requests
import json

st.set_page_config(
    page_title="Jet Suit Transport Agent",
    page_icon="🚀",
    layout="centered",
)

st.title("🛫 Jet-Suit Transport Agent: Fly Over Jakarta's Macet!")
st.markdown("""
**Powered by Gravity Industries Jet Suit**  
Escape traffic with turbine-powered flight 🏙️➡️🌤️
""")

# --- Secrets handling ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    api_key = os.getenv("OPENROUTER_API_KEY", "")

if not api_key:
    api_key = st.text_input("Enter your OpenRouter API Key:", type="password")
    if not api_key:
        st.warning("Need an OpenRouter API key? Get one free at openrouter.ai!")
        st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# System Prompt
SYSTEM_PROMPT = """
You are an Agentic AI Transport Planner for Gravity Industries' Jet Suit.
Specs: 80 mph, 3–9 min flights, ~$440k suit cost, fictional trip fee $50–$200.
Ideal for beating Jakarta, Bogor, Depok, Tangerang, Bekasi traffic.
1. Parse origin/destination/time.
2. Check feasibility.
3. Plan aerial route & time.
4. Highlight benefits.
5. Simulate booking.
Be concise & exciting.
"""

# Function to call OpenRouter API directly
def call_openrouter(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jet-suit-planner.streamlit.app/",
        "X-Title": "Jet Suit Transport Agent"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# User Input
user_input = st.chat_input("e.g., Fly from Depok to Jakarta Pusat avoiding rush hour")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("AI plotting your flight..."):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *st.session_state.messages
        ]
        reply = call_openrouter(messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown("---")
st.caption("Built with ❤️ for Jakarta skies")
