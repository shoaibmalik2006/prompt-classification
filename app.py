import streamlit as st
import pickle
import os
import time
from datetime import datetime

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Security VIP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# -------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'threats_detected' not in st.session_state:
    st.session_state.threats_detected = 0

# -------------------------------------------------
# ENHANCED CSS
# -------------------------------------------------
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Hero Section */
    .hero-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #555;
        margin-bottom: 0.5rem;
    }
    
    .hero-description {
        font-size: 1rem;
        color: #888;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.3rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Analysis Section */
    .analysis-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: slideIn 0.5s ease-out;
        height: 100%;
    }
    
    .result-card.safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .result-card.malicious {
        background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
    }
    
    .result-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .confidence-bar {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
        height: 10px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .confidence-fill {
        background: white;
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
    }
    
    /* History Section */
    .history-item {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .history-time {
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 0.5rem;
    }
    
    .history-text {
        font-size: 0.95rem;
        color: #333;
        margin-bottom: 0.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .history-results {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .history-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-ai {
        background: #667eea;
        color: white;
    }
    
    .badge-human {
        background: #38ef7d;
        color: white;
    }
    
    .badge-safe {
        background: #38ef7d;
        color: white;
    }
    
    .badge-malicious {
        background: #ff6a00;
        color: white;
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-top: 2rem;
    }
    
    .footer-text {
        font-size: 1rem;
        color: #666;
    }
    
    .footer-highlight {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
        }
        to {
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------
@st.cache_resource
def load_models():
    human_ai_model = pickle.load(open(os.path.join(MODEL_DIR, "human_ai_model.pkl"), "rb"))
    human_ai_vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "human_ai_vectorizer.pkl"), "rb"))
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

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🛡️ AI SECURITY VIP</div>
    <div class="hero-subtitle">Human vs AI & Malicious Prompt Detection</div>
    <div class="hero-description">
        Enterprise-grade security system powered by advanced machine learning algorithms.
        Detect AI-generated content and identify potential security threats in real-time.
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown(f"""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-icon">🔍</div>
        <div class="stat-value">{st.session_state.total_scans}</div>
        <div class="stat-label">Total Scans</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">⚠️</div>
        <div class="stat-value">{st.session_state.threats_detected}</div>
        <div class="stat-label">Threats Detected</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-value">{st.session_state.total_scans - st.session_state.threats_detected}</div>
        <div class="stat-label">Safe Scans</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-value">{len(st.session_state.history)}</div>
        <div class="stat-label">History Records</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Analysis Section
st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Text Analysis</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Enter text to analyze",
    height=200,
    placeholder="Paste your text here for comprehensive AI and security analysis...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze = st.button("🛡️ Analyze Now", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if analyze:
    if text_input.strip() == "":
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        with st.spinner("🔄 Analyzing your text..."):
            result = classify_text(text_input)
            
            # Update stats
            st.session_state.total_scans += 1
            if result['malicious_result'] == "Malicious":
                st.session_state.threats_detected += 1
            
            # Add to history
            st.session_state.history.insert(0, {
                "text": text_input[:100] + "..." if len(text_input) > 100 else text_input,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ai_result": result['ai_result'],
                "mal_result": result['malicious_result']
            })
            
            # Keep only last 10 items
            if len(st.session_state.history) > 10:
                st.session_state.history = st.session_state.history[:10]
        
        st.balloons()
        
        col1, col2 = st.columns(2)
        
        with col1:
            card_class = "result-card"
            icon = "🤖" if result['ai_result'] == "AI-Generated" else "👤"
            st.markdown(f"""
            <div class="{card_class}">
                <div class="result-icon">{icon}</div>
                <div class="result-title">AI Detection</div>
                <div class="result-value">{result['ai_result']}</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">
                    Confidence: {result['ai_confidence']:.2f}%
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {result['ai_confidence']:.0f}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            card_class = "result-card safe" if result['malicious_result'] == "Safe" else "result-card malicious"
            icon = "✅" if result['malicious_result'] == "Safe" else "🚨"
            st.markdown(f"""
            <div class="{card_class}">
                <div class="result-icon">{icon}</div>
                <div class="result-title">Threat Analysis</div>
                <div class="result-value">{result['malicious_result']}</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">
                    Confidence: {result['mal_confidence']:.2f}%
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {result['mal_confidence']:.0f}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1.5rem; color: white; font-size: 1rem;">
            ⏱ Processing Time: {result['time']:.3f}s
        </div>
        """, unsafe_allow_html=True)

# Sidebar - History
with st.sidebar:
    st.markdown('<div class="section-title">📜 Recent Scans</div>', unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.info("No scans yet. Start analyzing text to see history.")
    else:
        for item in st.session_state.history:
            ai_badge = "badge-ai" if item['ai_result'] == "AI-Generated" else "badge-human"
            mal_badge = "badge-safe" if item['mal_result'] == "Safe" else "badge-malicious"
            
            st.markdown(f"""
            <div class="history-item">
                <div class="history-time">🕐 {item['time']}</div>
                <div class="history-text">{item['text']}</div>
                <div class="history-results">
                    <span class="history-badge {ai_badge}">{item['ai_result']}</span>
                    <span class="history-badge {mal_badge}">{item['mal_result']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">
        ⚡ Built with passion by <span class="footer-highlight">Shoaib</span> 🚀
    </div>
    <div class="footer-text" style="margin-top: 0.5rem;">
        Semester-3 AI Security Project | Powered by Machine Learning
    </div>
</div>
""", unsafe_allow_html=True)
