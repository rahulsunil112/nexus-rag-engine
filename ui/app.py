import streamlit as st
import requests
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Nexus RAG Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #1f2937;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("Nexus Control")
    st.markdown("---")
    
    st.subheader("📚 Knowledge Base")
    uploaded_file = st.file_uploader("Upload Documents (PDF, TXT)", type=['pdf', 'txt'])
    
    if uploaded_file:
        if st.button("Ingest Document"):
            with st.spinner("Processing & Embedding..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    res = requests.post(f"{API_URL}/ingest", files=files)
                    if res.status_code == 200:
                        st.success(f"Successfully indexed: {uploaded_file.name}")
                    else:
                        st.error("Ingestion failed.")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    st.markdown("---")
    st.info("💡 **Tip:** Ask specific questions about your uploaded documents.")

# Main Interface
st.title("🧠 Nexus Enterprise RAG")
st.markdown("### Intelligent Search & Retrieval Engine")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Bot Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                payload = {"query": prompt, "top_k": 3}
                response = requests.post(f"{API_URL}/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer found.")
                    citations = data.get("citations", [])
                    latency = data.get("latency", 0.0)
                    
                    # Simulate streaming typing effect
                    for chunk in answer.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    
                    # Show metadata
                    with st.expander("🔍 View Sources & Latency"):
                        st.caption(f"Latency: {latency}s")
                        for idx, ref in enumerate(citations):
                            st.markdown(f"**[{idx+1}] Source:** {ref.get('source', 'unknown')} (Page {ref.get('page', '?')})")
                else:
                    st.error("Error connecting to backend.")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})