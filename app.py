import streamlit as st
import requests
import time

# --- 1. SETTINGS & ADVANCED CUSTOM UI ---
st.set_page_config(page_title="NovaWave | Intelligent CX", layout="wide")

# Custom CSS for a professional "SaaS" look
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8f9fa; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1c1c1c !important;
        color: white;
    }
    
    /* Chat Bubble Styling */
    .stChatMessage {
        background-color: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }
    
    /* Metrics / Dashboard Cards */
    .metric-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-top: 5px solid #D0191F;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        text-align: center;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        background-color: #D0191F;
        color: white;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #A01317; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE AI ENGINE (Connected to Secrets) ---
def get_ai_response(user_input):
    # This pulls the token from the "Secrets" you saved in Streamlit Cloud settings
    try:
        token = st.secrets["HF_TOKEN"]
    except:
        return "⚠️ CONFIG ERROR: HF_TOKEN not found in Secrets. Please add it in Streamlit Cloud Settings."

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"}
    
    system_prompt = (
        "You are the NovaWave AI Assistant. NovaWave is a telecom company. "
        "Case Facts: Pranav is a Gold Member. $10 fees are for paper bills (waivable). "
        "Roaming is $15. Unlimited plan is $80. "
        "Instructions: Use empathy and PwC values (Clarity). Be concise. Think step-by-step."
    )
    
    payload = {"inputs": f"<s>[INST] {system_prompt} User: {user_input} [/INST]"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        raw_output = response.json()
        
        # This handles the AI thinking
        if isinstance(raw_output, list) and len(raw_output) > 0:
            return raw_output[0]['generated_text'].split("[/INST]")[-1].strip()
        else:
            return "I am currently analyzing your account details. Could you please specify the billing month?"
    except:
        return "I'm experiencing a high load on my neural engine. Let me check your Gold Member benefits manually... how can I help with that charge?"

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/PricewaterhouseCoopers_Logo.svg", width=80)
    st.markdown("### **NovaWave Portal**")
    st.markdown("---")
    page = st.radio("SELECT VIEW", ["📊 DASHBOARD", "🤖 AI ASSISTANT", "📜 TICKET HISTORY"])

# --- 4. PAGE LOGIC ---

# PAGE: DASHBOARD
if page == "📊 DASHBOARD":
    st.title("Strategic Account Overview")
    st.markdown("Welcome back, **Pranav**. Here is your real-time account status.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card">Current Bill<br><h1>$95.00</h1><span style="color:red">+$15.00 vs Feb</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card">Data Usage<br><h1>18.2 GB</h1><span style="color:orange">91% Capacity</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card">Loyalty Tier<br><h1>GOLD</h1><span style="color:green">Full Waiver Access</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💡 Proactive AI Insight")
    st.success("Our AI detected an unusual $15 roaming charge. We recommend using 'AI Assistant' to request an automated waiver before the billing cycle ends.")

# PAGE: AI ASSISTANT
elif page == "🤖 AI ASSISTANT":
    st.title("NovaWave Intelligent Assistant")
    st.caption("Empowered by Mistral-7B Large Language Model")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display History
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("Explain your issue..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI is reasoning..."):
                time.sleep(1) # Visual polish
                answer = get_ai_response(prompt)
                st.markdown(answer)
        
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# PAGE: TICKETS
elif page == "📜 TICKET HISTORY":
    st.title("Case Management History")
    st.table([
        {"Ticket ID": "NW-1021", "Issue": "Slow Fiber Speed", "Status": "Resolved", "Method": "AI Auto-Fix"},
        {"Ticket ID": "NW-1150", "Issue": "Bill Discrepancy", "Status": "Pending", "Method": "Agent Review"}
    ])
