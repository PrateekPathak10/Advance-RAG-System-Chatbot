from Generation.query_rewrite import rewrite_query
from Retriever.retriever import get_docs
from Generation.prompt import build_prompt
from utils.cache import get_cached, set_cache
from utils.logger import log_query


def is_summary_query(query):
    keywords = ["summary", "summarize", "overview"]
    return any(k in query.lower() for k in keywords)


def summarize_document(llm, vector_db):
    docs = vector_db.similarity_search("", k=20)

    #remove duplicates
    unique_docs = list({d.page_content: d for d in docs}.values())

    context = "\n\n".join([d.page_content for d in unique_docs])

    prompt = f"""
Summarize the following document in a clear and structured way:

{context}

Summary:
"""

    response = llm.invoke(prompt)

    return {
        "query": "summary",
        "improved_query": "Document Summary Mode",
        "answer": response.content,
        "sources": [doc.metadata for doc in unique_docs[:3]]
    }


def run_rag_pipeline(query, llm, vector_db, all_docs):

    
    cached = get_cached(query)
    if cached:
        return cached

    log_query(query)

    # SUMMARY MODE
    if is_summary_query(query):
        result = summarize_document(llm, vector_db)
        set_cache(query, result)
        return result

    # Query rewrite
    improved_query = rewrite_query(llm, query)

    # Retrieval
    docs = get_docs(vector_db, all_docs, improved_query)

    # remove duplicates
    docs = list({d.page_content: d for d in docs}.values())

    # Context
    context = "\n\n".join([
        f"[Source {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])

    # Generate
    prompt = build_prompt(context, query)
    response = llm.invoke(prompt)

    result = {
        "query": query,
        "improved_query": improved_query,
        "answer": response.content,
        "sources": [doc.metadata for doc in docs]
    }

    set_cache(query, result)

    return result