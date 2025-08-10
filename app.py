import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="Jet-Suit Planner",
    page_icon="🚀",
)

st.title("🛩️ Jet-Suit Transport Agent")
st.caption("Escape Jakarta’s macet with turbine-powered flight!")

# ------------------------------------------------------------------
# 1) API key from Streamlit Secrets (no text_input, no leaks)
# ------------------------------------------------------------------
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    st.error(
        "Missing `OPENROUTER_API_KEY` in `.streamlit/secrets.toml`. "
        "Please add it and reboot the app."
    )
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ------------------------------------------------------------------
# 2) Chat memory
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM = """
You are an agentic Jet-Suit transport planner.
Specs: 80 mph, 3–9 min flights, ~$440 k suit, fictional trip fee $50–$200.
Ideal for beating Jakarta/Bogor/Depok/Tangerang/Bekasi traffic.
1) Parse origin/destination.
2) Check feasibility.
3) Plan aerial route & ETA.
4) Highlight benefits.
5) Simulate booking.
Be concise & exciting.
"""

# ------------------------------------------------------------------
# 3) Chat UI
# ------------------------------------------------------------------
user_input = st.chat_input("e.g., Fly from Depok to Jakarta Pusat at 5 pm")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("AI plotting flight…"):
        try:
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "system", "content": SYSTEM}]
                + st.session_state.messages,
                max_tokens=500,
                temperature=0.7,
            )
            reply = res.choices[0].message.content
        except Exception as e:
            reply = f"Oops! OpenRouter error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": reply})

# display history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
