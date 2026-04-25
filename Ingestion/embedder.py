from langchain_community.embeddings import HuggingFaceEmbeddings

import os

def get_embedded():
    ENV = os.getenv("ENV", "local")

    if ENV == "production":
        # ightweight for deployment
        from langchain_community.embeddings import FakeEmbeddings
        return FakeEmbeddings(size=384)

    else:
        # real embeddings for local
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )