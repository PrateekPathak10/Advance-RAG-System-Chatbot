from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_docs(docs):
    splitter= RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100
        )
    chunks= splitter.split_documents(docs)
    return chunks[:150]