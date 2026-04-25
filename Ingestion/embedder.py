import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

def get_embedded():
    return HuggingFaceInferenceAPIEmbeddings(
        api_key=os.getenv("HF_TOKEN"),
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )