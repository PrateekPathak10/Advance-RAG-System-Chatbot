from langchain_chroma import Chroma

def create_vector_store(chunks, embeddings):

    db = Chroma(
        persist_directory="./db",
        embedding_function=embeddings
    )

    batch_size = 64

    for i in range(0, len(chunks), batch_size):
        db.add_documents(chunks[i:i+batch_size])

    return db