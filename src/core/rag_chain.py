from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from src.core.llm_config import get_llm, get_embeddings

VECTORSTORE_DIR = "vectorstore"

template = """You are a helpful corporate AI assistant. 
Use the following context to answer the question.
Context:
{context}

Question: {question}

Helpful Answer:"""

def query_agent(query: str):
    """
    Queries the RAG agent and returns the response and source documents.
    """
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(template)
    
    formatted_prompt = prompt.format(context=context, question=query)
    response = llm.invoke(formatted_prompt)
    
    # Retornar respuesta y metadatos de los documentos
    return response.content, docs
