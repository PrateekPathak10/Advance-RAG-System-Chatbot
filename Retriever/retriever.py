from Retriever.reranker import rerank_docs
from Retriever.hybrid import keyword_search

def get_docs(vector_db,all_docs, query):

    semantic_docs = vector_db.similarity_search(query, k=3)

    if not all_docs:
        return semantic_docs[:3]

    keyword_docs = keyword_search(all_docs, query)

    combined = list({id(doc): doc for doc in semantic_docs + keyword_docs}.values())

    final_docs= rerank_docs(query, combined)

    return final_docs