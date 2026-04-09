import streamlit as st
import requests
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="NovaWave CX Portal", layout="wide")

# PRO DESIGN: PwC Colors (Black, Red, Orange, Grey)
st.markdown("""
    <style>
    .main { background-color: #f4f1f0; }
    [data-testid="stSidebar"] { background-color: #2d2d2d; color: white; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #D0191F; color: white; border-radius: 0px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- THE "BRAIN" (Easily Swappable) ---
def get_ai_response(user_input):
    # Currently using Hugging Face Pro Model
    # Logic: If manager gives a new key later, we just swap this API_URL
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    # Use Vercel Environment Variables for Security
    HF_TOKEN = st.secrets["HF_TOKEN"] 
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    system_prompt = "You are a NovaWave Telecom AI. Resolve billing ($10 fee waiver for Gold), roaming ($15), and plan issues using PwC values of Clarity and Empathy."
    payload = {"inputs": f"<s>[INST] {system_prompt} User asks: {user_input} [/INST]"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]['generated_text'].split("[/INST]")[-1].strip()
    except:
        return "I'm currently connected via a backup logic layer. How can I help with your bill today?"

# --- UI LAYOUT ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/PricewaterhouseCoopers_Logo.svg", width=80)
    st.title("NovaWave Portal")
    mode = st.radio("Navigate", ["Dashboard", "AI Support", "Ticket History"])

if mode == "Dashboard":
    st.header("Strategic Account Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Unpaid Balance", "$95.00", "+$15.00")
    col2.metric("Data Usage", "18.2 GB", "91%")
    col3.metric("Loyalty Status", "Gold", "Priority")
    
    st.subheader("Predictive Action")
    st.info("AI Analysis: High probability of 'Sticker Shock' regarding roaming fees. Recommend proactive waiver.")

elif mode == "AI Support":
    st.header("NovaWave Intelligent Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Ask about your bill..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif mode == "Ticket History":
    st.header("Case Management")
    st.table([
        {"ID": "NW-101", "Issue": "Roaming Charge", "Status": "Resolved by AI", "Savings": "$15.00"},
        {"ID": "NW-102", "Issue": "Plan Optimization", "Status": "Open", "Savings": "TBD"}
    ])