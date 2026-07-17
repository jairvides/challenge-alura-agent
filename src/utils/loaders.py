import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    CSVLoader, 
    JSONLoader, 
    UnstructuredMarkdownLoader, 
    BSHTMLLoader
)
import pandas as pd

def load_document(file_path: str) -> List[Document]:
    """
    Loads a document based on its file extension.
    Supported formats: .pdf, .docx, .xlsx, .csv, .json, .html, .md
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
            return loader.load()
        
        elif ext == '.docx':
            loader = Docx2txtLoader(file_path)
            return loader.load()
        
        elif ext == '.csv':
            loader = CSVLoader(file_path)
            return loader.load()
        
        elif ext == '.json':
            # Assuming JSON is a list of objects or a simple structure
            # For a generic corporate agent, we'll use a simple JSON loader
            loader = JSONLoader(
                file_path=file_path,
                jq_schema='.[]', 
                text_content=False
            )
            return loader.load()
        
        elif ext == '.html':
            loader = BSHTMLLoader(file_path)
            return loader.load()
        
        elif ext == '.md':
            loader = UnstructuredMarkdownLoader(file_path)
            return loader.load()
        
        elif ext in ['.xlsx', '.xls']:
            # Excel doesn't have a simple single-file loader that always works well
            # We'll use pandas to read all sheets and convert to Documents
            df_dict = pd.read_excel(file_path, sheet_name=None)
            docs = []
            for sheet_name, df in df_dict.items():
                content = df.to_string()
                docs.append(Document(page_content=content, metadata={"source": file_path, "sheet": sheet_name}))
            return docs
        
        else:
            print(f"Unsupported file extension: {ext}")
            return []
            
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return []

def load_all_documents(data_dir: str) -> List[Document]:
    """
    Traverses the data directory and loads all supported documents.
    """
    all_docs = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_docs.extend(load_document(file_path))
    return all_docs
