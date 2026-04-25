from rank_bm25 import BM25Okapi

def keyword_search(docs, query):
    corpus = [doc.page_content.split() for doc in docs]
    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(query.split())
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:5]]