import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from retriever import retrieve, chunks
from generator import generate_answer

st.set_page_config(
    page_title="DocBot — eBay Agreement Assistant",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }
    
    section[data-testid="stSidebar"] {
        background-color: #1a1d27;
        border-right: 1px solid #2d3048;
    }
    
    .brand-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    
    .brand-sub {
        font-size: 12px;
        color: #8b92a5;
        margin-bottom: 24px;
    }
    
    .info-card {
        background: #22253a;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 12px;
        border: 1px solid #2d3048;
    }
    
    .info-label {
        font-size: 11px;
        font-weight: 600;
        color: #8b92a5;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 2px;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
    }
    
    .chat-header h1 {
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        color: white;
    }
    
    .chat-header p {
        font-size: 14px;
        opacity: 0.85;
        margin: 6px 0 0 0;
        color: white;
    }
    
    [data-testid="stChatMessage"] {
        background-color: #1a1d27 !important;
        border-radius: 12px !important;
        border: 1px solid #2d3048 !important;
        margin-bottom: 8px !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #e2e8f0 !important;
    }
    
    .stChatInputContainer {
        background-color: #1a1d27 !important;
        border-top: 1px solid #2d3048 !important;
        padding-top: 16px !important;
    }
    
    div[data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 2px solid #2d3048 !important;
        background: #22253a !important;
        color: #ffffff !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }
    
    .source-badge {
        display: inline-block;
        background: #2d3048;
        color: #a78bfa;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 8px;
        border: 1px solid #3d4070;
    }

    .source-text {
        color: #cbd5e1 !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
    }
    
    details {
        background-color: #22253a !important;
        border: 1px solid #2d3048 !important;
        border-radius: 10px !important;
        padding: 4px !important;
    }
    
    details summary {
        color: #a78bfa !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    details * {
        color: #cbd5e1 !important;
    }

    .suggested-btn button {
        background-color: #22253a !important;
        color: #a78bfa !important;
        border: 1px solid #2d3048 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: 100% !important;
        text-align: left !important;
    }

    .clear-btn button {
        background-color: #2d1a1a !important;
        color: #f87171 !important;
        border: 1px solid #5a2020 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        width: 100% !important;
    }

    p, span, div, li {
        color: #e2e8f0;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    hr {
        border-color: #2d3048 !important;
    }

    [data-testid="stSidebarContent"] p,
    [data-testid="stSidebarContent"] span,
    [data-testid="stSidebarContent"] div {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="brand-title">📄 DocBot</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">AI-powered document assistant</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-card"><div class="info-label">Model</div><div class="info-value">LLaMA 3.1 8B</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card"><div class="info-label">Document</div><div class="info-value">eBay User Agreement</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><div class="info-label">Indexed Chunks</div><div class="info-value">{len(chunks)} chunks</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card"><div class="info-label">Vector DB</div><div class="info-value">FAISS</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**💡 Suggested Questions**")

    suggested = [
        "What is eBay's return policy?",
        "How does Money Back Guarantee work?",
        "What is the arbitration process?",
        "Can I sell vehicles on eBay?",
    ]

    for s in suggested:
        st.markdown('<div class="suggested-btn">', unsafe_allow_html=True)
        if st.button(s, key=s):
            st.session_state.suggested_query = s
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main chat area
st.markdown("""
<div class="chat-header">
    <h1>📄 eBay Agreement Assistant</h1>
    <p>Ask me anything about the eBay User Agreement — I'll find the answer from the document.</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_query" not in st.session_state:
    st.session_state.suggested_query = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question about the eBay User Agreement...")

if st.session_state.suggested_query:
    query = st.session_state.suggested_query
    st.session_state.suggested_query = None

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    retrieved_chunks = retrieve(query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream = generate_answer(query, retrieved_chunks)
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            full_response += token
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        with st.expander("📎 View Source Passages"):
            for i, c in enumerate(retrieved_chunks):
                st.markdown(f'<div class="source-badge">Source {i+1}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="source-text">{c}</p>', unsafe_allow_html=True)
                if i < len(retrieved_chunks) - 1:
                    st.divider()

    st.session_state.messages.append({"role": "assistant", "content": full_response})