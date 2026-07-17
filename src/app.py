import streamlit as st
import os
from src.core.rag_chain import query_agent
from src.utils.validator import validate_file
from ingest import perform_ingestion

st.set_page_config(page_title="Corporate AI Agent", page_icon="🤖", layout="wide")

# CSS para fijar el selector de idioma en la parte superior derecha
st.markdown("""
<style>
div[data-testid="stAppViewContainer"] > section > div {
    padding-top: 0rem;
}
div[data-testid="stVerticalBlock"]:has(div[data-testid="stRadio"]) {
    position: fixed;
    top: 0.5rem;
    right: 1rem;
    z-index: 1000;
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🤖 E-CommCorp Knowledge Agent")
with col2:
    st.markdown("")  # Columna vacía, el selector se renderiza fijo por CSS

# Selector fijo (se renderiza aquí pero flota gracias al CSS)
language = st.radio("Idioma", ["Spanish", "English"], horizontal=True, key="lang_selector")

# Sidebar para gestión de documentos
with st.sidebar:
    st.header("Gestionar Documentos")
    uploaded_file = st.file_uploader("Subir nueva política", type=['pdf', 'docx', 'csv', 'json', 'md', 'html', 'xlsx'])
    
    if uploaded_file:
        save_path = os.path.join("data", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        is_valid, msg = validate_file(save_path)
        if is_valid:
            st.success(msg)
            if st.button("Procesar archivo"):
                with st.spinner("Ingestando..."):
                    if perform_ingestion():
                        st.success("Archivo procesado!")
        else:
            st.error(msg)
            os.remove(save_path)

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Fuentes"):
                for src in message["sources"]:
                    st.write(f"- {src}")

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response, docs = query_agent(prompt, language=language)
        sources = list(set([doc.metadata.get('source', 'Desconocido') for doc in docs]))
        
        st.markdown(response)
        with st.expander("Fuentes"):
            for src in sources:
                st.write(f"- {src}")
        
        st.session_state.messages.append({"role": "assistant", "content": response, "sources": sources})
