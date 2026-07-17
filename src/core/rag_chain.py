from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from src.core.llm_config import get_llm, get_embeddings

VECTORSTORE_DIR = "vectorstore"

# Prompt
template = """You are a helpful corporate AI assistant for an E-commerce company. 
Use the following pieces of retrieved context to answer the user's question. 
If you don't know the answer based on the context, just say that you don't know.
Keep the answer concise and professional.

Context:
{context}

Question: {question}

Helpful Answer:"""

def query_agent(query: str) -> str:
    """
    Queries the RAG agent manually.
    """
    embeddings = get_embeddings()
    
    # 1. Cargar vector store
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # 2. Recuperar documentos
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 3. Generar respuesta
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(template)
    
    # Definir formatted_prompt correctamente
    formatted_prompt = prompt.format(context=context, question=query)
    response = llm.invoke(formatted_prompt)
    
    # Retornar el contenido de la respuesta
    return response.content
