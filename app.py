import streamlit as st
import pickle
import os
import time

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Security VIP",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .main-title {text-align: center; font-size: 4rem; font-weight: 900; background: linear-gradient(90deg, #a855f7, #ec4899, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .subtitle {text-align: center; color: #9ca3af; font-size: 1.2rem; margin-bottom: 2rem;}
    .security-badge {text-align: center; color: #10b981; font-weight: 600; margin-bottom: 3rem;}
    .main-card {background: rgba(30,27,75,0.8); backdrop-filter: blur(20px); border-radius: 30px; padding: 2rem; border: 2px solid rgba(168,85,247,0.3); margin-bottom: 2rem;}
    .result-card {border-radius: 20px; padding: 1.5rem; border: 2px solid; margin-bottom: 1rem;}
    .ai-generated {border-color: #a855f7;}
    .human-generated {border-color: #3b82f6;}
    .malicious {border-color: #ef4444;}
    .safe {border-color: #10b981;}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------
@st.cache_resource
def load_models():
    # New Human vs AI model
    human_ai_model = pickle.load(open(os.path.join(MODEL_DIR, "human_ai_model.pkl"), "rb"))
    human_ai_vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "human_ai_vectorizer.pkl"), "rb"))
    # Malicious model remains the same
    malicious_model = pickle.load(open(os.path.join(MODEL_DIR, "malicious_model.pkl"), "rb"))
    malicious_vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "malicious_vectorizer.pkl"), "rb"))
    return human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer

human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer = load_models()

# -------------------------------------------------
# CLASSIFICATION FUNCTION
# -------------------------------------------------
def classify_text(text):
    start = time.time()

    # Human vs AI
    ai_vec = human_ai_vectorizer.transform([text])
    ai_pred = human_ai_model.predict(ai_vec)[0]
    ai_proba = human_ai_model.predict_proba(ai_vec)[0]
    ai_result = "AI-Generated" if ai_pred == 1 else "Human-Generated"
    ai_confidence = ai_proba[ai_pred] * 100

    # Malicious Detection
    mal_vec = malicious_vectorizer.transform([text])
    mal_pred = malicious_model.predict(mal_vec)[0]
    mal_proba = malicious_model.predict_proba(mal_vec)[0]
    mal_result = "Malicious" if mal_pred == 1 else "Safe"
    mal_confidence = mal_proba[mal_pred] * 100

    return {
        "ai_result": ai_result,
        "ai_confidence": ai_confidence,
        "malicious_result": mal_result,
        "mal_confidence": mal_confidence,
        "time": time.time() - start
    }

# -------------------------------------------------
# UI
# -------------------------------------------------
load_css()
st.markdown("""
<div class="main-title">🛡️ AI SECURITY</div>
<div class="subtitle">Human vs AI & Malicious Prompt Detection</div>
<div class="security-badge">🔒 Enterprise-Grade Security System</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
text_input = st.text_area("Enter text to analyze", height=200, placeholder="Paste text here...")
analyze = st.button("🛡️ Analyze Now", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# RESULTS
# -------------------------------------------------
if analyze:
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            result = classify_text(text_input)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="result-card {'ai-generated' if result['ai_result']=='AI-Generated' else 'human-generated'}">
                <h4>🤖 AI Detection</h4>
                <h2>{result['ai_result']}</h2>
                <p>Confidence: {result['ai_confidence']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="result-card {'malicious' if result['malicious_result']=='Malicious' else 'safe'}">
                <h4>🔥 Threat Analysis</h4>
                <h2>{result['malicious_result']}</h2>
                <p>Confidence: {result['mal_confidence']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"⏱ Processing Time: {result['time']:.3f}s")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<hr>
<div style="text-align:center;color:#9ca3af;">
Built by <b>Shoaib</b> 🚀 | Semester-3 AI Security Project
</div>
""", unsafe_allow_html=True)
