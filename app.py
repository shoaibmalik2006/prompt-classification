import streamlit as st import pickle import os import time from datetime import datetime # ------------------------------------------------- # STREAMLIT CONFIG # ------------------------------------------------- st.set_page_config( page_title="AI Security Project", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded" ) # ------------------------------------------------- # PATHS # ------------------------------------------------- BASE_DIR = os.path.dirname(os.path.abspath(__file__)) MODEL_DIR = os.path.join(BASE_DIR, "models") # Debug: Check if directory exists if not os.path.exists(MODEL_DIR): st.error(f"❌ Models directory not found: {MODEL_DIR}") st.stop() # ------------------------------------------------- # SESSION STATE INITIALIZATION # ------------------------------------------------- if 'history' not in st.session_state: st.session_state.history = [] if 'total_scans' not in st.session_state: st.session_state.total_scans = 0 if 'threats_detected' not in st.session_state: st.session_state.threats_detected = 0 if 'models_loaded' not in st.session_state: st.session_state.models_loaded = False # ------------------------------------------------- # ENHANCED CSS # ------------------------------------------------- def load_css(): st.markdown(""" """, unsafe_allow_html=True) # ------------------------------------------------- # LOAD MODELS WITH ERROR HANDLING # ------------------------------------------------- @st.cache_resource def load_models(): try: model_files = { "human_ai_model.pkl": None, "human_ai_vectorizer.pkl": None, "malicious_model.pkl": None, "malicious_vectorizer.pkl": None } # Check if all files exist for filename in model_files.keys(): filepath = os.path.join(MODEL_DIR, filename) if not os.path.exists(filepath): raise FileNotFoundError(f"Model file not found: {filename}") # Load models human_ai_model_path = os.path.join(MODEL_DIR, "human_ai_model.pkl") human_ai_vectorizer_path = os.path.join(MODEL_DIR, "human_ai_vectorizer.pkl") malicious_model_path = os.path.join(MODEL_DIR, "malicious_model.pkl") malicious_vectorizer_path = os.path.join(MODEL_DIR, "malicious_vectorizer.pkl") with open(human_ai_model_path, "rb") as f: human_ai_model = pickle.load(f) with open(human_ai_vectorizer_path, "rb") as f: human_ai_vectorizer = pickle.load(f) with open(malicious_model_path, "rb") as f: malicious_model = pickle.load(f) with open(malicious_vectorizer_path, "rb") as f: malicious_vectorizer = pickle.load(f) return human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer, None except Exception as e: return None, None, None, None, str(e) # Load models human_ai_model, human_ai_vectorizer, malicious_model, malicious_vectorizer, error = load_models() # ------------------------------------------------- # CLASSIFICATION FUNCTION # ------------------------------------------------- def classify_text(text): start = time.time() # Human vs AI ai_vec = human_ai_vectorizer.transform([text]) ai_pred = human_ai_model.predict(ai_vec)[0] ai_proba = human_ai_model.predict_proba(ai_vec)[0] ai_result = "AI-Generated" if ai_pred == 1 else "Human-Generated" ai_confidence = ai_proba[ai_pred] * 100 # Malicious Detection mal_vec = malicious_vectorizer.transform([text]) mal_pred = malicious_model.predict(mal_vec)[0] mal_proba = malicious_model.predict_proba(mal_vec)[0] mal_result = "Malicious" if mal_pred == 1 else "Safe" mal_confidence = mal_proba[mal_pred] * 100 return { "ai_result": ai_result, "ai_confidence": ai_confidence, "malicious_result": mal_result, "mal_confidence": mal_confidence, "time": time.time() - start } # ------------------------------------------------- # UI # ------------------------------------------------- load_css() # Check for model loading errors if error: st.markdown("""
🛡️ AI SECURITY PROJECT
Model Loading Error
 """, unsafe_allow_html=True) st.error("❌ **Failed to load models**") st.markdown(f"""
🔍 Troubleshooting Information:
Error Details: {error}
Expected Directory: {MODEL_DIR}
Required Files:
* human_ai_model.pkl
* human_ai_vectorizer.pkl
* malicious_model.pkl
* malicious_vectorizer.pkl
 """, unsafe_allow_html=True) # Show existing files if os.path.exists(MODEL_DIR): files = os.listdir(MODEL_DIR) st.info(f"📁 **Files found in models directory:** {', '.join(files) if files else 'None'}") st.markdown(""" ### 🔧 **Solutions:** 1. **Verify model files exist** in the `models/` directory 2. **Re-train and save models** using the same Python version 3. **Check file permissions** and ensure files are not corrupted 4. **Use absolute paths** if relative paths aren't working 5. **Regenerate pickle files** with compatible pickle protocol ### 💡 **Quick Fix:** ```python # Save models with compatibility import pickle with open('model.pkl', 'wb') as f: pickle.dump(model, f, protocol=4) # Use protocol 4 for compatibility ``` """) st.stop() # Hero Section st.markdown("""
🛡️ AI SECURITY PROJECT
Human vs AI & Malicious Prompt Detection
 Enterprise-grade security system powered by advanced machine learning algorithms. Detect AI-generated content and identify potential security threats in real-time.
 """, unsafe_allow_html=True) # Stats Section st.markdown(f"""
🔍
{st.session_state.total_scans}
Total Scans
⚠️
{st.session_state.threats_detected}
Threats Detected
✅
{st.session_state.total_scans - st.session_state.threats_detected}
Safe Scans
⚡
{len(st.session_state.history)}
History Records
 """, unsafe_allow_html=True) # Analysis Section st.markdown('
', unsafe_allow_html=True) st.markdown('
📝 Text Analysis
', unsafe_allow_html=True) text_input = st.text_area( "Enter text to analyze", height=200, placeholder="Paste your text here for comprehensive AI and security analysis...", label_visibility="collapsed" ) col1, col2, col3 = st.columns([1, 2, 1]) with col2: analyze = st.button("🛡️ Analyze Now", use_container_width=True) st.markdown('
', unsafe_allow_html=True) # Results Section if analyze: if text_input.strip() == "": st.warning("⚠️ Please enter some text to analyze.") else: with st.spinner("🔄 Analyzing your text..."): result = classify_text(text_input) # Update stats st.session_state.total_scans += 1 if result['malicious_result'] == "Malicious": st.session_state.threats_detected += 1 # Add to history st.session_state.history.insert(0, { "text": text_input[:100] + "..." if len(text_input) > 100 else text_input, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ai_result": result['ai_result'], "mal_result": result['malicious_result'] }) # Keep only last 10 items if len(st.session_state.history) > 10: st.session_state.history = st.session_state.history[:10] st.balloons() col1, col2 = st.columns(2) with col1: card_class = "result-card" icon = "🤖" if result['ai_result'] == "AI-Generated" else "👤" st.markdown(f"""
{icon}
AI Detection
{result['ai_result']}
 Confidence: {result['ai_confidence']:.2f}%
 """, unsafe_allow_html=True) with col2: card_class = "result-card safe" if result['malicious_result'] == "Safe" else "result-card malicious" icon = "✅" if result['malicious_result'] == "Safe" else "🚨" st.markdown(f"""
{icon}
Threat Analysis
{result['malicious_result']}
 Confidence: {result['mal_confidence']:.2f}%
 """, unsafe_allow_html=True) st.markdown(f"""
 ⏱ Processing Time: {result['time']:.3f}s
 """, unsafe_allow_html=True) # Sidebar - History with st.sidebar: st.markdown('
📜 Recent Scans
', unsafe_allow_html=True) if len(st.session_state.history) == 0: st.info("No scans yet. Start analyzing text to see history.") else: for item in st.session_state.history: ai_badge = "badge-ai" if item['ai_result'] == "AI-Generated" else "badge-human" mal_badge = "badge-safe" if item['mal_result'] == "Safe" else "badge-malicious" st.markdown(f"""
🕐 {item['time']}
{item['text']}
{item['ai_result']} {item['mal_result']}
 """, unsafe_allow_html=True) if st.button("🗑️ Clear History", use_container_width=True): st.session_state.history = [] st.rerun() # Footer st.markdown("""
 ⚡ Built with passion by Shoaib Malik 🚀
 Semester-3 AI Security Project | Powered by Machine Learning
 """, unsafe_allow_html=True)                       
