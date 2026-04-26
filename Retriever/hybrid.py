from rank_bm25 import BM25Okapi

# Cache so BM25 index is built once, not on every query
_bm25_index = None
_bm25_docs = None


def build_bm25_index(docs):
    global _bm25_index, _bm25_docs
    corpus = [doc.page_content.split() for doc in docs]
    _bm25_index = BM25Okapi(corpus)
    _bm25_docs = docs


def keyword_search(docs, query):
    global _bm25_index, _bm25_docs

    # Rebuild only if docs have changed 
    if _bm25_index is None or _bm25_docs is not docs:
        build_bm25_index(docs)

    scores = _bm25_index.get_scores(query.split())
    ranked = sorted(zip(_bm25_docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:5]]