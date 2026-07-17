from typing import List
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from src.core.llm_config import get_llm, get_embeddings

VECTORSTORE_DIR = "vectorstore"

# Custom Prompt Template
template = """You are a helpful corporate AI assistant for an E-commerce company. 
Use the following pieces of retrieved context to answer the user's question. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Keep the answer concise and professional.

Context:
{context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

def get_rag_chain():
    """
    Constructs and returns the RAG chain.
    """
    embeddings = get_embeddings()
    
    # Load the persisted vector store
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    llm = get_llm()
    
    # Create the retrieval chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return chain

def query_agent(query: str) -> str:
    """
    Queries the RAG agent and returns the response string.
    """
    chain = get_rag_chain()
    response = chain.invoke({"query": query})
    return response["result"]
