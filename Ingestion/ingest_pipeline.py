import os
from Ingestion.loader import load_pdf
from Ingestion.chunks import split_docs
from Ingestion.embedder import get_embedded
from Retriever.vector_store import create_vector_store



def ingest_pdf(file_path, embeddings):

    docs= load_pdf(file_path)

    for i, doc in enumerate(docs):
        doc.metadata["source"]= os.path.basename(file_path)
        doc.metadata["chunk_id"]= i

    # Split
    chunks= split_docs(docs)



    # Store
    vector_db= create_vector_store(chunks, embeddings)

    return len(chunks)