import streamlit as st
import os
from openai import OpenAI
import traceback

# Set page config
st.set_page_config(
    page_title="Jet Suit Transport Agent",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# App Title with Futuristic Flair
st.title("🛫 Jet-Suit Transport Agent: Fly Over Jakarta's Macet!")
st.markdown("""
**Powered by Gravity Industries Jet Suit + OpenAI**  
Escape traffic with turbine-powered flight 🏙️➡️🌤️
""")

# --- Secrets handling (works on both Streamlit Cloud & Vercel) ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    api_key = os.getenv("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ API Key Missing! Please add your OpenRouter API key in app settings")
    api_key = st.text_input(
        "Enter your OpenRouter API Key:", 
        type="password",
        help="Get your free API key at openrouter.ai"
    )
    if not api_key:
        st.stop()

# Set Up OpenAI-Compatible Client for OpenRouter
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://jet-suit-planner.streamlit.app/",
            "X-Title": "Jet Suit Transport Agent"
        }
    )
    # Test connection
    with st.spinner("Connecting to AI..."):
        test_response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=1
        )
except Exception as e:
    st.error(f"🚫 Connection Error: {str(e)}")
    st.info("Please check your API key and internet connection")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# System Prompt: Make AI Agentic for Jet Suit Transport
SYSTEM_PROMPT = """
You are an Agentic AI Transport Planner for Gravity Industries' Jet Suit—a revolutionary alternative to ojek, taksi, buses, and KRL in Jabodetabek, Indonesia. 
The Jet Suit uses arm/back turbines for human flight: speeds up to 80 mph, 3-9 min flights, costs ~$440K/suit (fictional trip fees: $50-200). 
It's ideal for avoiding traffic, density, and macet in areas like Jakarta, Bogor, Depok, Tangerang, Bekasi.
Act agentically: 
1. Analyze user query (origin, destination, time).
2. Check feasibility (short distances, no regulations mentioned).
3. Plan route: Aerial path, est. time (e.g., 5 mins vs. 2 hours by car).
4. Suggest benefits: Faster, exciting, eco-thrills.
5. "Book" simulation: Confirm details.
6. If unclear, ask questions.
Keep responses exciting, innovative, and concise!
"""

# User Input
user_input = st.chat_input(
    "Your trip query (e.g., From Jakarta Selatan to Bandara Soekarno-Hatta):",
    key="chat_input"
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate AI Response
    try:
        with st.spinner("AI Agent Planning Your Flight... 🚀"):
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",  # Using a stable free model
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                max_tokens=500,
                temperature=0.7,
            )
            ai_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        error_message = f"⚠️ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.error(error_message)
        print(traceback.format_exc())  # Log error for debugging

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Footer
st.markdown("---")
st.caption("Built with ❤️ for Jakarta skies | v1.0")
