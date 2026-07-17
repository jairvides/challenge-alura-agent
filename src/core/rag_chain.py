from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from src.core.llm_config import get_llm, get_embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import time

VECTORSTORE_DIR = "vectorstore"

template = """You are BimBam Buy's Expert Policy Assistant. 
Your tone is professional, clear, and aligned with BimBam Buy's brand: friendly, dynamic, and reliable.
Use the provided retrieved context (policies, warranties, shipping guides) to give authoritative answers.

If you don't know the answer based on the context, politely inform the user, explain what you don't know, and suggest they contact official support channels if necessary.
When applicable, refer the user to specific document sections or follow-up actions defined in the policy.
Respond in the following language: {language}.

Context:
{context}

Question: {question}

Helpful Answer:"""

def query_agent(query: str, language: str = "Spanish"):
    try:
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        
        llm = get_llm()
        prompt = ChatPromptTemplate.from_template(template)
        formatted_prompt = prompt.format(context=context, question=query, language=language)
        
        response = llm.invoke(formatted_prompt)
        text_response = response.text if hasattr(response, 'text') else response.content
        
        return text_response, docs
    except Exception as e:
        if "429" in str(e):
            return "Lo siento, hemos alcanzado el límite de uso gratuito de la API. Por favor, intenta de nuevo en un minuto.", []
        return f"Ocurrió un error inesperado: {str(e)}", []
