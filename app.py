import streamlit as st
import pickle
import os
import time
from datetime import datetime

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Security Project",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

if not os.path.exists(MODEL_DIR):
    st.error(f"❌ Models directory not found: {MODEL_DIR}")
    st.stop()

# -------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'threats_detected' not in st.session_state:
    st.session_state.threats_detected = 0
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False
if 'show_examples' not in st.session_state:
    st.session_state.show_examples = False
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = "Single Text"
if 'confidence_threshold' not in st.session_state:
    st.session_state.confidence_threshold = 50.0

# -------------------------------------------------
# ENHANCED CSS WITH ANIMATIONS
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
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        text-align: center;
        animation: fadeInUp 0.8s ease-out;
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
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: titlePulse 2s ease-in-out infinite;
    }
    
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #555;
        margin-bottom: 1rem;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
        cursor: pointer;
    }
    
    .stat-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
    }
    
    .analysis-section {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        animation: slideIn 0.8s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        animation: resultAppear 0.5s ease-out;
    }
    
    @keyframes resultAppear {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .result-card:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .result-card.safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        box-shadow: 0 10px 30px rgba(56, 239, 125, 0.4);
    }
    
    .result-card.malicious {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        box-shadow: 0 10px 30px rgba(235, 51, 73, 0.4);
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: iconPop 0.6s ease-out;
    }
    
    @keyframes iconPop {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .result-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .confidence-bar {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
        height: 12px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .confidence-fill {
        background: white;
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
        animation: fillBar 1s ease-out;
    }
    
    @keyframes fillBar {
        from { width: 0%; }
    }
    
    .history-item {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .history-item:hover {
        transform: translateX(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-ai {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .badge-human {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .badge-safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .badge-malicious {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
    
    .example-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .example-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .processing-animation {
        text-align: center;
        padding: 2rem;
    }
    
    .spinner {
        border: 8px solid #f3f3f3;
        border-top: 8px solid #667eea;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    .progress-text {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        text-align: center;
        font-weight: 600;
        color: #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        border-radius: 15px;
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# LOAD MODELS WITH ERROR HANDLING
# -------------------------------------------------
@st.cache_resource
def load_models():
    try:
        model_files = {
            "human_ai_model.pkl": None,
            "human_ai_vectorizer.pkl": None,
            "malicious_model.pkl": None,
            "malicious_vectorizer.pkl": None
        }

        for filename in model_files.keys():
            filepath = os.path.join(MODEL_DIR, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model file not found: {filename}")

        human_ai_model_path = os.path.join(MODEL_DIR, "human_ai_model.pkl")
        human_ai_vectorizer_path = os.path.join(MODEL_DIR, "human_ai_vectorizer.pkl")
        malicious_model_path = os.path.join(MODEL_DIR, "malicious_model.pkl")
        malicious_vectorizer_path = os.path.join(MODEL_DIR, "malicious_vectorizer.pkl")

        with open(human_ai_model_path, "rb") as f:
            human_ai_model = pickle.load(f)
        with open(human_ai_vectorizer_path, "rb") as f:
            human_ai_vectorizer = pickle.load(f)
        with open(malicious_model_path, "rb") as f:
            malicious_model = pickle.load(f)
        with open(malicious_vectorizer_path, "rb") as f:
            malicious_vectorizer = pickle.load(f)

        return human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer, None
    except Exception as e:
        return None, None, None, None, str(e)

human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer, error = load_models()

# -------------------------------------------------
# CLASSIFICATION FUNCTION
# -------------------------------------------------
def classify_text(text):
    start = time.time()
    
    ai_vec = human_ai_vectorizer.transform([text])
    ai_pred = human_ai_model.predict(ai_vec)[0]
    ai_proba = human_ai_model.predict_proba(ai_vec)[0]
    ai_result = "AI-Generated" if ai_pred == 1 else "Human-Generated"
    ai_confidence = ai_proba[ai_pred] * 100
    
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
# VISUALIZATION FUNCTIONS (Using Native HTML/CSS)
# -------------------------------------------------
def create_confidence_gauge_html(confidence, title, color="#667eea"):
    return f"""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #333; margin-bottom: 1rem;">{title}</h3>
        <div style="position: relative; width: 200px; height: 200px; margin: 0 auto;">
            <svg viewBox="0 0 200 200" style="transform: rotate(-90deg);">
                <circle cx="100" cy="100" r="80" fill="none" stroke="#e0e0e0" stroke-width="20"/>
                <circle cx="100" cy="100" r="80" fill="none" stroke="{color}" stroke-width="20"
                        stroke-dasharray="{confidence * 5.02} 502" 
                        style="transition: stroke-dasharray 1s ease-out;"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 2rem; font-weight: bold; color: {color};">
                {confidence:.1f}%
            </div>
        </div>
    </div>
    """

def create_history_chart_html():
    if len(st.session_state.history) == 0:
        return None
    
    ai_counts = {"AI-Generated": 0, "Human-Generated": 0}
    mal_counts = {"Safe": 0, "Malicious": 0}
    
    for item in st.session_state.history:
        ai_counts[item['ai_result']] += 1
        mal_counts[item['mal_result']] += 1
    
    max_count = max(max(ai_counts.values()), max(mal_counts.values()))
    
    return f"""
    <div style="background: white; border-radius: 15px; padding: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">Analysis Distribution</h3>
        <div style="margin-bottom: 1.5rem;">
            <h4 style="color: #666; font-size: 0.9rem;">AI Detection</h4>
            <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
                <span style="width: 120px; font-size: 0.85rem;">AI-Generated:</span>
                <div style="flex: 1; background: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                    <div style="width: {(ai_counts['AI-Generated']/max_count*100) if max_count > 0 else 0}%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; transition: width 1s ease-out; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; font-weight: bold;">
                        {ai_counts['AI-Generated']}
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <span style="width: 120px; font-size: 0.85rem;">Human-Written:</span>
                <div style="flex: 1; background: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                    <div style="width: {(ai_counts['Human-Generated']/max_count*100) if max_count > 0 else 0}%; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); height: 100%; transition: width 1s ease-out; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; font-weight: bold;">
                        {ai_counts['Human-Generated']}
                    </div>
                </div>
            </div>
        </div>
        <div>
            <h4 style="color: #666; font-size: 0.9rem;">Threat Analysis</h4>
            <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
                <span style="width: 120px; font-size: 0.85rem;">Safe:</span>
                <div style="flex: 1; background: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                    <div style="width: {(mal_counts['Safe']/max_count*100) if max_count > 0 else 0}%; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); height: 100%; transition: width 1s ease-out; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; font-weight: bold;">
                        {mal_counts['Safe']}
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <span style="width: 120px; font-size: 0.85rem;">Malicious:</span>
                <div style="flex: 1; background: #e0e0e0; border-radius: 5px; height: 25px; overflow: hidden;">
                    <div style="width: {(mal_counts['Malicious']/max_count*100) if max_count > 0 else 0}%; background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); height: 100%; transition: width 1s ease-out; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; font-weight: bold;">
                        {mal_counts['Malicious']}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

# -------------------------------------------------
# EXAMPLE TEXTS
# -------------------------------------------------
EXAMPLE_TEXTS = {
    "AI-Generated (Safe)": "Artificial intelligence is revolutionizing various industries by enabling machines to perform tasks that typically require human intelligence. Machine learning algorithms can analyze vast amounts of data to identify patterns and make predictions.",
    "Human-Written (Safe)": "Hey! Just wanted to let you know that I'll be a bit late for our meeting today. Traffic is crazy on Main Street. See you around 3pm instead of 2:30pm. Thanks for understanding!",
    "Potentially Malicious": "Click here to claim your prize NOW!!! You've won $1,000,000 in our lottery. Send your bank details immediately to: suspicious@fake-site.com. This offer expires in 24 hours! ACT FAST!!!",
    "Technical (Safe)": "To implement the binary search algorithm, first ensure the array is sorted. Then, repeatedly divide the search interval in half. Compare the middle element with the target value and adjust the interval accordingly until the element is found or the interval is empty."
}

# -------------------------------------------------
# UI
# -------------------------------------------------
load_css()

if error:
    st.markdown("""<div class="hero-section">
        <div class="hero-title">🛡️ AI SECURITY PROJECT</div>
        <div class="hero-subtitle">Model Loading Error</div>
    </div>""", unsafe_allow_html=True)
    st.error("❌ **Failed to load models**")
    st.markdown(f"""**Error:** {error}  
**Directory:** {MODEL_DIR}  
**Required Files:** human_ai_model.pkl, human_ai_vectorizer.pkl, malicious_model.pkl, malicious_vectorizer.pkl""")
    st.stop()

# Hero Section with Animation
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🛡️ AI SECURITY PROJECT</div>
    <div class="hero-subtitle">Human vs AI & Malicious Prompt Detection</div>
    <p style="font-size: 1.1rem; color: #777; max-width: 800px; margin: 0 auto;">
        Enterprise-grade security system powered by advanced machine learning algorithms. 
        Detect AI-generated content and identify potential security threats in real-time.
    </p>
</div>
""", unsafe_allow_html=True)

# Interactive Stats Section with Hover Effects
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

# Tabs for Different Modes
tab1, tab2, tab3 = st.tabs(["📝 Single Analysis", "📊 Batch Analysis", "💡 Examples & Info"])

with tab1:
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Text Analysis</div>', unsafe_allow_html=True)
    
    # Settings
    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area(
            "Enter text to analyze",
            height=200,
            placeholder="Paste your text here for comprehensive AI and security analysis...",
            key="main_text_input"
        )
    with col2:
        st.markdown("### ⚙️ Settings")
        st.session_state.confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 100.0, 50.0, 5.0,
            help="Set minimum confidence level for alerts"
        )
        show_details = st.checkbox("Show Detailed Analysis", value=True)
        live_typing = st.checkbox("Enable Live Analysis", value=False)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze = st.button("🛡️ Analyze Now", use_container_width=True, key="analyze_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results Section with Enhanced Visualization
    if analyze:
        if text_input.strip() == "":
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            # Animated Processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.markdown('<div class="progress-text">🔍 Analyzing text patterns...</div>', unsafe_allow_html=True)
                elif i < 60:
                    status_text.markdown('<div class="progress-text">🤖 Running AI detection...</div>', unsafe_allow_html=True)
                elif i < 90:
                    status_text.markdown('<div class="progress-text">🛡️ Checking for threats...</div>', unsafe_allow_html=True)
                else:
                    status_text.markdown('<div class="progress-text">✅ Finalizing results...</div>', unsafe_allow_html=True)
                time.sleep(0.01)
            
            result = classify_text(text_input)
            progress_bar.empty()
            status_text.empty()
            
            # Update stats
            st.session_state.total_scans += 1
            if result['malicious_result'] == "Malicious":
                st.session_state.threats_detected += 1
            
            # Add to history
            st.session_state.history.insert(0, {
                "text": text_input[:100] + "..." if len(text_input) > 100 else text_input,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ai_result": result['ai_result'],
                "mal_result": result['malicious_result'],
                "ai_confidence": result['ai_confidence'],
                "mal_confidence": result['mal_confidence']
            })
            
            if len(st.session_state.history) > 10:
                st.session_state.history = st.session_state.history[:10]
            
            st.balloons()
            
            # Results Display
            col1, col2 = st.columns(2)
            
            with col1:
                card_class = "result-card"
                icon = "🤖" if result['ai_result'] == "AI-Generated" else "👤"
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="result-icon">{icon}</div>
                    <div class="result-title">AI Detection</div>
                    <div class="result-value">{result['ai_result']}</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {result['ai_confidence']}%;"></div>
                    </div>
                    <p style="margin-top: 1rem; font-size: 1.1rem;">Confidence: {result['ai_confidence']:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                if show_details:
                    st.markdown(create_confidence_gauge_html(result['ai_confidence'], "AI Detection Confidence", "#667eea"), unsafe_allow_html=True)
            
            with col2:
                card_class = "result-card safe" if result['malicious_result'] == "Safe" else "result-card malicious"
                icon = "✅" if result['malicious_result'] == "Safe" else "🚨"
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="result-icon">{icon}</div>
                    <div class="result-title">Threat Analysis</div>
                    <div class="result-value">{result['malicious_result']}</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {result['mal_confidence']}%;"></div>
                    </div>
                    <p style="margin-top: 1rem; font-size: 1.1rem;">Confidence: {result['mal_confidence']:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                if show_details:
                    gauge_color = "#38ef7d" if result['malicious_result'] == "Safe" else "#eb3349"
                    st.markdown(create_confidence_gauge_html(result['mal_confidence'], "Threat Detection Confidence", gauge_color), unsafe_allow_html=True)
            
            # Additional Insights
            if show_details:
                st.markdown("---")
                st.markdown("### 📊 Detailed Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Processing Time", f"{result['time']:.3f}s", delta="Fast")
                with col2:
                    st.metric("Text Length", f"{len(text_input)} chars")
                with col3:
                    risk_level = "High" if result['mal_result'] == "Malicious" else "Low"
                    st.metric("Risk Level", risk_level)

with tab2:
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Batch Analysis</div>', unsafe_allow_html=True)
    
    st.info("💡 Analyze multiple texts at once by entering them separated by '---'")
    
    batch_input = st.text_area(
        "Enter multiple texts (separate with '---')",
        height=300,
        placeholder="Text 1\n---\nText 2\n---\nText 3",
        key="batch_input"
    )
    
    if st.button("🚀 Analyze Batch", use_container_width=True):
        if batch_input.strip():
            texts = [t.strip() for t in batch_input.split('---') if t.strip()]
            
            if len(texts) > 0:
                results = []
                progress = st.progress(0)
                
                for i, text in enumerate(texts):
                    result = classify_text(text)
                    results.append({
                        'text': text[:50] + '...',
                        'ai': result['ai_result'],
                        'ai_conf': result['ai_confidence'],
                        'mal': result['malicious_result'],
                        'mal_conf': result['mal_confidence']
                    })
                    progress.progress((i + 1) / len(texts))
                    st.session_state.total_scans += 1
                    if result['malicious_result'] == "Malicious":
                        st.session_state.threats_detected += 1
                
                progress.empty()
                st.success(f"✅ Analyzed {len(texts)} texts successfully!")
                
                # Display results in a table
                st.markdown("### 📋 Batch Results")
                for idx, res in enumerate(results, 1):
                    with st.expander(f"Text {idx}: {res['text']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**AI Detection:** {res['ai']}")
                            st.progress(res['ai_conf'] / 100)
                            st.caption(f"Confidence: {res['ai_conf']:.2f}%")
                        with col2:
                            st.markdown(f"**Threat Analysis:** {res['mal']}")
                            st.progress(res['mal_conf'] / 100)
                            st.caption(f"Confidence: {res['mal_conf']:.2f}%")
            else:
                st.warning("⚠️ No valid texts found. Please separate texts with '---'")
        else:
            st.warning("⚠️ Please enter some text to analyze")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Examples & Information</div>', unsafe_allow_html=True)
    
    st.markdown("### 📚 Try These Examples")
    st.markdown("Click on any example to analyze it:")
    
    for title, text in EXAMPLE_TEXTS.items():
        if st.button(f"📄 {title}", key=f"example_{title}", use_container_width=True):
            st.session_state.example_text = text
            st.rerun()
    
    if hasattr(st.session_state, 'example_text'):
        st.markdown("---")
        st.markdown("### Selected Example:")
        st.text_area("Example Text", st.session_state.example_text, height=150, key="example_display")
        
        if st.button("🛡️ Analyze This Example", use_container_width=True):
            result = classify_text(st.session_state.example_text)
            
            st.session_state.total_scans += 1
            if result['malicious_result'] == "Malicious":
                st.session_state.threats_detected += 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">{"🤖" if result['ai_result'] == "AI-Generated" else "👤"}</div>
                    <div class="result-title">AI Detection</div>
                    <div class="result-value">{result['ai_result']}</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {result['ai_confidence']}%;"></div>
                    </div>
                    <p style="margin-top: 1rem;">Confidence: {result['ai_confidence']:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                card_class = "result-card safe" if result['malicious_result'] == "Safe" else "result-card malicious"
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="result-icon">{"✅" if result['malicious_result'] == "Safe" else "🚨"}</div>
                    <div class="result-title">Threat Analysis</div>
                    <div class="result-value">{result['malicious_result']}</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {result['mal_confidence']}%;"></div>
                    </div>
                    <p style="margin-top: 1rem;">Confidence: {result['mal_confidence']:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📖 How It Works")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🤖 AI Detection
        Our system uses advanced machine learning models to distinguish between:
        - **AI-Generated Text**: Content created by language models
        - **Human-Written Text**: Content written by real people
        
        The model analyzes patterns, vocabulary, and structure to make predictions.
        """)
    
    with col2:
        st.markdown("""
        #### 🛡️ Threat Detection
        The malicious content detector identifies:
        - **Phishing Attempts**: Suspicious links and requests
        - **Spam Content**: Unsolicited promotional messages
        - **Social Engineering**: Manipulation tactics
        - **Harmful Instructions**: Dangerous or unethical content
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Best Practices")
    st.info("""
    **Tips for Accurate Analysis:**
    - Provide at least 50 characters for better accuracy
    - Include complete sentences when possible
    - Context matters - longer texts yield better results
    - The model works best with English text
    - Confidence scores above 80% are highly reliable
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Sidebar with Visualizations
with st.sidebar:
    st.markdown('<div class="section-title">📜 Recent Scans</div>', unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.info("No scans yet. Start analyzing text to see history.")
    else:
        # Show history chart
        chart_html = create_history_chart_html()
        if chart_html:
            st.markdown(chart_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        for idx, item in enumerate(st.session_state.history):
            ai_badge = "badge-ai" if item['ai_result'] == "AI-Generated" else "badge-human"
            mal_badge = "badge-safe" if item['mal_result'] == "Safe" else "badge-malicious"
            
            st.markdown(f"""
            <div class="history-item">
                <div style="font-size: 0.8rem; color: #999; margin-bottom: 0.5rem;">
                    🕐 {item['time']}
                </div>
                <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
                    {item['text']}
                </div>
                <div>
                    <span class="badge {ai_badge}">{item['ai_result']}</span>
                    <span class="badge {mal_badge}">{item['mal_result']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    with col2:
        if st.button("🔄 Reset Stats", use_container_width=True):
            st.session_state.total_scans = 0
            st.session_state.threats_detected = 0
            st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
        ⚡ Built with passion by Shoaib Malik 🚀
    </p>
    <p style="color: #666;">
        Semester-3 AI Security Project | Powered by Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)
