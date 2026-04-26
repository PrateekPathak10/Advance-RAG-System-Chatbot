# import os
# from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

# def get_embedded():
#     return HuggingFaceInferenceAPIEmbeddings(
#         api_key=os.getenv("HF_TOKEN"),
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )


from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

"""Replaced HuggingFaceInferenceAPIEmbeddings (external API call per batch)
 with FastEmbedEmbeddings which runs locally on CPU much faster on Render."""

def get_embedded():
    return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")