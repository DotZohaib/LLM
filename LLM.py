import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom CSS for modern dark theme
def inject_custom_css():
    st.markdown("""
    <style>
       
    </style>
    """, unsafe_allow_html=True)

def configure_gemini():
    """Configure Gemini API and return model"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ API Key Not Configured")
        return None
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"🔴 Initialization Error: {str(e)}")
        return None

def generate_response(model, question):
    """Generate response using Gemini model"""
    try:
        with st.spinner("🌀 Generating magic..."):
            response = model.generate_content(question)
            return response.text
    except Exception as e:
        st.error(f"🚨 Generation Error: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Nexus AI",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    inject_custom_css()

    # Initialize session state
    if 'model' not in st.session_state:
        st.session_state.model = configure_gemini()

    # Input Section
    with st.container():
        col1, col2 = st.columns([6, 1])
        with col1:
            question = st.text_input(
                " ",
                placeholder="💡 Ask me anything...",
                key="user_input",
                label_visibility="collapsed"
            )
        with col2:
            submit_btn = st.button("🚀 Send", use_container_width=True)

    # Handle submission
    if submit_btn or question:
        if not question.strip():
            st.warning("📝 Please enter your query")
            return

        if st.session_state.model is None:
            st.error("❌ Model Not Initialized")
            return

        response = generate_response(st.session_state.model, question)
        
        if response:
            with st.container():
                st.markdown("""<div class="response-card">""", unsafe_allow_html=True)
                st.markdown("### 🌟 AI Response")
                st.markdown("---")
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()