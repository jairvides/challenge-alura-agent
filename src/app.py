import streamlit as st
import os
from src.core.rag_chain import query_agent
from src.utils.validator import validate_file
from ingest import perform_ingestion

st.set_page_config(page_title="Corporate AI Agent", page_icon="🤖")

st.title("🤖 E-CommCorp Knowledge Agent")

# Sidebar
with st.sidebar:
    st.header("Configuración")
    # Selector de idioma
    language = st.radio("Idioma de respuesta", ["Spanish", "English"], index=0)
    
    st.header("Gestionar Documentos")
    uploaded_file = st.file_uploader("Subir nueva política", type=['pdf', 'docx', 'csv', 'json', 'md', 'html', 'xlsx'])
    
    if uploaded_file:
        save_path = os.path.join("data", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Validar
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
        # Pasamos el idioma seleccionado
        response, docs = query_agent(prompt, language=language)
        sources = list(set([doc.metadata.get('source', 'Desconocido') for doc in docs]))
        
        st.markdown(response)
        with st.expander("Fuentes"):
            for src in sources:
                st.write(f"- {src}")
        
        st.session_state.messages.append({"role": "assistant", "content": response, "sources": sources})
