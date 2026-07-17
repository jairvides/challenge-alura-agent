import os
from langchain_community.llms import OCIGenAI
from langchain_community.embeddings import OCIGenAIEmbeddings

def get_llm():
    """
    Returns OCI Generative AI model using Instance Principal auth.
    """
    return OCIGenAI(
        model_id="cohere.command-r-plus",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id=os.getenv("OCI_COMPARTMENT_ID"),
        auth_type="INSTANCE_PRINCIPAL",
        model_kwargs={"temperature": 0},
    )

def get_embeddings():
    """
    Returns OCI Generative AI embeddings model.
    """
    return OCIGenAIEmbeddings(
        model_id="cohere.embed-english-v3.0",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id=os.getenv("OCI_COMPARTMENT_ID"),
        auth_type="INSTANCE_PRINCIPAL",
    )
