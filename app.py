import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="Jet Suit Transport Agent",
    page_icon="🚀",
    layout="centered",
)

st.title("🛫 Jet-Suit Transport Agent: Fly Over Jakarta’s Macet!")
st.markdown(
    """
    **Powered by Gravity Industries Jet Suit + Qwen AI**  
    Escape traffic with turbine-powered flight 🏙️➡️🌤️
    """
)

# --- Secrets handling (works on both Streamlit Cloud & Vercel) ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    api_key = st.text_input(
        "Enter your OpenRouter API Key:", type="password"
    ) or st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM = """
You are an agentic AI transport planner for Gravity Industries' Jet Suit.  
Specs: 80 mph, 3–9 min flights, ~$440k suit cost, fictional trip fee $50–$200.  
Ideal for beating Jakarta, Bogor, Depok, Tangerang, Bekasi traffic.  
1. Parse origin/destination/time.  
2. Check feasibility.  
3. Plan aerial route & time.  
4. Highlight benefits.  
5. Simulate booking.  
Be concise & exciting.
"""

user_input = st.chat_input(
    "e.g., Fly from Depok to Jakarta Pusat avoiding rush hour"
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI plotting your flight..."):
        res = client.chat.completions.create(
            model="qwen/qwen-2.5-72b-instruct",
            messages=[{"role": "system", "content": SYSTEM}]
            + st.session_state.messages,
            max_tokens=500,
            temperature=0.7,
        )
        reply = res.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown("---")
st.caption("Built with ❤️ for Jakarta skies")
