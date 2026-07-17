import os
from src.utils.loaders import load_all_documents
from src.core.llm_config import get_embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"

def main():
    print("Starting ingestion process...")
    
    # 1. Load Documents
    docs = load_all_documents(DATA_DIR)
    if not docs:
        print("No documents found in data directory. Exiting.")
        return
    
    print(f"Loaded {len(docs)} documents.")
    
    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")
    
    # 3. Generate Embeddings and Create Vector Store
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    # 4. Persist Index
    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"Vector store saved to {VECTORSTORE_DIR}")

if __name__ == "__main__":
    main()
