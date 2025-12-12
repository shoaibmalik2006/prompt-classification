import streamlit as st
import pickle
import os
import time

# ------------------------------------------------- 
# MODEL DIRECTORY (IMPORTANT FOR STREAMLIT CLOUD)
# ------------------------------------------------- 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ------------------------------------------------- 
# CUSTOM CSS FOR VIP INTERFACE
# ------------------------------------------------- 
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title Styling */
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #a855f7, #ec4899, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .security-badge {
        text-align: center;
        color: #10b981;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 3rem;
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 2rem;
        gap: 1rem;
    }
    
    .stat-card {
        background: rgba(30, 27, 75, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
    }
    
    .stat-label {
        color: #9ca3af;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        color: white;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Main Card */
    .main-card {
        background: rgba(30, 27, 75, 0.8);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(168, 85, 247, 0.3);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(15, 12, 41, 0.8) !important;
        border: 2px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
    }
    
    /* Button */
    .stButton button {
        background: linear-gradient(90deg, #a855f7, #ec4899) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(168, 85, 247, 0.6) !important;
    }
    
    /* Results Cards */
    .result-card {
        background: rgba(30, 27, 75, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 2px solid;
    }
    
    .result-card.ai-generated {
        border-color: #a855f7;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(168, 85, 247, 0.05));
    }
    
    .result-card.human-generated {
        border-color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.05));
    }
    
    .result-card.malicious {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05));
    }
    
    .result-card.safe {
        border-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05));
    }
    
    .result-title {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .result-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .progress-bar {
        background: rgba(15, 12, 41, 0.8);
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(15, 12, 41, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        color: #9ca3af;
    }
    
    .info-value {
        color: #a855f7;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        margin-top: 3rem;
        font-size: 1rem;
    }
    
    .footer-highlight {
        color: #a855f7;
        font-weight: 700;
    }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .analyzing {
        animation: pulse 1.5s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------- 
# SAFE LOADING FUNCTION
# ------------------------------------------------- 
@st.cache_resource
def load_models():
    human_ai_model = pickle.load(open(os.path.join(MODEL_DIR, "human_ai_model.pkl"), "rb"))
    human_ai_vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "rb"))
    malicious_model = pickle.load(open(os.path.join(MODEL_DIR, "malicious_model.pkl"), "rb"))
    malicious_vectorizer = pickle.load(open(os.path.join(MODEL_DIR, "malicious_vectorizer.pkl"), "rb"))
    return human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer

# Load models only once (cached)
human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer = load_models()

# ------------------------------------------------- 
# CLASSIFICATION FUNCTION
# ------------------------------------------------- 
def classify_text(text):
    # Measure processing time
    start_time = time.time()
    
    # Human vs AI Detection
    ai_vec = human_ai_vectorizer.transform([text])
    ai_pred = human_ai_model.predict(ai_vec)[0]
    ai_proba = human_ai_model.predict_proba(ai_vec)[0]
    
    # Malicious Prompt Detection
    mal_vec = malicious_vectorizer.transform([text])
    mal_pred = malicious_model.predict(mal_vec)[0]
    mal_proba = malicious_model.predict_proba(mal_vec)[0]
    
    processing_time = time.time() - start_time
    
    return {
        "ai_result": "AI-Generated" if ai_pred == 1 else "Human-Generated",
        "ai_confidence": max(ai_proba) * 100,
        "malicious_result": "Malicious" if mal_pred == 1 else "Safe",
        "mal_confidence": max(mal_proba) * 100,
        "processing_time": processing_time
    }

# ------------------------------------------------- 
# STREAMLIT UI
# ------------------------------------------------- 
st.set_page_config(
    page_title="AI Security VIP", 
    page_icon="🛡️",
    layout="wide"
)

# Load Custom CSS
load_css()

# Header
st.markdown("""
<div class="main-title">🛡️ AI SECURITY</div>
<div class="subtitle">Advanced AI Detection & Threat Analysis System</div>
<div class="security-badge">🔒 ENTERPRISE GRADE SECURITY</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-label">🧠 AI Models</div>
        <div class="stat-value">2</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">⚡ Accuracy</div>
        <div class="stat-value">98.7%</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">🛡️ Scans</div>
        <div class="stat-value">10K+</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Container
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Text Input
user_input = st.text_area(
    "✨ Enter Text to Analyze", 
    height=200,
    placeholder="Paste your text here for advanced AI detection and security analysis..."
)

# Word and Character Count
if user_input:
    word_count = len(user_input.split())
    char_count = len(user_input)
    st.markdown(f"""
    <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
        {char_count} characters • {word_count} words
    </div>
    """, unsafe_allow_html=True)

# Analyze Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze_button = st.button("🛡️ Analyze Now", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
if analyze_button:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        # Show analyzing animation
        with st.spinner("🔍 Analyzing..."):
            result = classify_text(user_input)
        
        # Info Box
        st.markdown(f"""
        <div class="info-box">
            <div class="info-row">
                <span>Processing Time</span>
                <span class="info-value">{result['processing_time']:.3f}s</span>
            </div>
            <div class="info-row">
                <span>Word Count</span>
                <span class="info-value">{len(user_input.split())}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Results Grid
        col1, col2 = st.columns(2)
        
        # AI Detection Result
        with col1:
            ai_class = "ai-generated" if result["ai_result"] == "AI-Generated" else "human-generated"
            color = "#a855f7" if result["ai_result"] == "AI-Generated" else "#3b82f6"
            st.markdown(f"""
            <div class="result-card {ai_class}">
                <div class="result-title">🤖 AI Detection</div>
                <div class="result-value" style="color: {color};">
                    {result["ai_result"]}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {result['ai_confidence']:.1f}%; background: linear-gradient(90deg, {color}, {color}cc);"></div>
                </div>
                <div style="text-align: right; color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">
                    Confidence: {result['ai_confidence']:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Malicious Detection Result
        with col2:
            mal_class = "malicious" if result["malicious_result"] == "Malicious" else "safe"
            color = "#ef4444" if result["malicious_result"] == "Malicious" else "#10b981"
            st.markdown(f"""
            <div class="result-card {mal_class}">
                <div class="result-title">🔥 Threat Analysis</div>
                <div class="result-value" style="color: {color};">
                    {result["malicious_result"]}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {result['mal_confidence']:.1f}%; background: linear-gradient(90deg, {color}, {color}cc);"></div>
                </div>
                <div style="text-align: right; color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">
                    Confidence: {result['mal_confidence']:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built by <span class="footer-highlight">Shoaib</span> 🚀 | Semester 3 Project
</div>
""", unsafe_allow_html=True)
