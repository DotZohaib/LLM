import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Custom CSS for modern dark theme
def inject_custom_css():
    st.markdown("""
    <style>
    .sidebar .chat-title {
        font-size: 14px;
        margin: 2px 0;
        cursor: pointer;
    }
    .sidebar .chat-item:hover {
        background-color: #2d2d2d;
    }
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
    }
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

# Chat storage functions
def load_chats():
    try:
        with open('chat_history.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chats(chats):
    with open('chat_history.json', 'w') as f:
        json.dump(chats, f)

def create_new_chat():
    st.session_state.current_chat = {
        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
        'title': 'New Chat',
        'messages': []
    }

def generate_chat_title(prompt):
    return prompt[:30] + "..." if len(prompt) > 30 else prompt

def handle_chat_edit(chat_id):
    st.session_state.editing_chat = chat_id

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
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()

    # Initialize session state
    if 'model' not in st.session_state:
        st.session_state.model = configure_gemini()
    
    if 'all_chats' not in st.session_state:
        st.session_state.all_chats = load_chats()
    
    if 'current_chat' not in st.session_state:
        create_new_chat()
    
    if 'editing_chat' not in st.session_state:
        st.session_state.editing_chat = None

    # Sidebar for chat history
    with st.sidebar:
        st.header("Chat History")
        
        # New Chat button
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat()
            st.session_state.editing_chat = None
        
        # Chat list
        for chat in reversed(st.session_state.all_chats):
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                    f"💬 {chat['title']}",
                    key=f"btn_{chat['id']}",
                    use_container_width=True,
                    help="Click to load chat"
                ):
                    st.session_state.current_chat = chat.copy()
                    st.session_state.editing_chat = None
            with col2:
                if st.button("✏️", key=f"edit_{chat['id']}", help="Edit chat"):
                    handle_chat_edit(chat['id'])

    # Main chat interface
    st.title("🤖 Nexus AI")
    
    # Edit mode handling
    if st.session_state.editing_chat:
        edited_chat = next(
            (chat for chat in st.session_state.all_chats 
             if chat['id'] == st.session_state.editing_chat), None)
        
        if edited_chat:
            st.subheader("✍️ Edit Chat")
            new_title = st.text_input("Chat Title", value=edited_chat['title'])
            new_messages = []
            
            for i, msg in enumerate(edited_chat['messages']):
                role = st.selectbox(
                    f"Role {i+1}",
                    ["user", "ai"],
                    index=0 if msg['role'] == "user" else 1,
                    key=f"role_{i}"
                )
                content = st.text_area(
                    f"Message {i+1}",
                    value=msg['content'],
                    key=f"content_{i}"
                )
                new_messages.append({"role": role, "content": content})
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("💾 Save Changes"):
                    edited_chat['title'] = new_title
                    edited_chat['messages'] = new_messages
                    save_chats(st.session_state.all_chats)
                    st.success("Chat updated!")
                    st.session_state.editing_chat = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel Edit"):
                    st.session_state.editing_chat = None
                    st.rerun()
    else:
        # Display current chat messages
        for msg in st.session_state.current_chat['messages']:
            with st.chat_message(name=msg['role']):
                st.write(msg['content'])

        # Input Section
        with st.container():
            question = st.chat_input("💡 Ask me anything...")
            
            if question and st.session_state.model:
                # Add user question to history
                st.session_state.current_chat['messages'].append({
                    "role": "user",
                    "content": question
                })
                
                # Generate response
                response = generate_response(st.session_state.model, question)
                
                if response:
                    # Add AI response to history
                    st.session_state.current_chat['messages'].append({
                        "role": "ai",
                        "content": response
                    })
                    
                    # Update chat title if first message
                    if len(st.session_state.current_chat['messages']) == 2:
                        st.session_state.current_chat['title'] = generate_chat_title(question)
                    
                    # Auto-save chat
                    if st.session_state.current_chat not in st.session_state.all_chats:
                        st.session_state.all_chats.append(st.session_state.current_chat.copy())
                        save_chats(st.session_state.all_chats)
                    
                    st.rerun()

        # Save button for existing chats
        if st.session_state.current_chat['messages']:
            if st.button("💾 Save Chat", use_container_width=True):
                if st.session_state.current_chat not in st.session_state.all_chats:
                    st.session_state.all_chats.append(st.session_state.current_chat.copy())
                    save_chats(st.session_state.all_chats)
                    st.success("Chat saved!")

if __name__ == "__main__":
    main()
