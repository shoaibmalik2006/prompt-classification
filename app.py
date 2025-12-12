import streamlit as st
import pickle
import os

# -------------------------------------------------
# MODEL DIRECTORY (IMPORTANT FOR STREAMLIT CLOUD)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

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

    # Human vs AI Detection
    ai_vec = human_ai_vectorizer.transform([text])
    ai_pred = human_ai_model.predict(ai_vec)[0]

    # Malicious Prompt Detection
    mal_vec = malicious_vectorizer.transform([text])
    mal_pred = malicious_model.predict(mal_vec)[0]  # 0 = safe, 1 = malicious

    return {
        "ai_result": "AI-Generated" if ai_pred == 1 else "Human-Generated",
        "malicious_result": "Malicious" if mal_pred == 1 else "Safe"
    }


# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
st.set_page_config(page_title="AI Security Project", page_icon="🚨")

st.title("🚨 AI SECURITY PROJECT")
st.write("Detect whether a text is AI-generated and check if it is malicious.")

st.markdown("---")

# Text Input
user_input = st.text_area("Enter text to analyze:", height=140)

# Analyze Button
if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("⚠ Please enter some text.")
    else:
        result = classify_text(user_input)

        st.subheader("🔍 Analysis Results")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🤖 Human vs AI")
            if result["ai_result"] == "AI-Generated":
                st.success("AI-Generated")
            else:
                st.info("Human-Generated")

        with col2:
            st.markdown("### 🔥 Malicious Prompt Detection")
            if result["malicious_result"] == "Malicious":
                st.error("Malicious Prompt")
            else:
                st.success("Safe Prompt")

st.markdown("---")
st.write("Built by **Shoaib** 🚀 | Semester 3 Project")
