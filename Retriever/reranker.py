import os

ENV = os.getenv("ENV", "local")

#PRODUCTION (LIGHTWEIGHT)
if ENV == "production":

    def rerank_docs(query, docs):
        # simple fallback (no heavy models)
        return docs[:3]


#LOCAL(HIGH QUALITY)
else:
    from sentence_transformers import CrossEncoder

    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank_docs(query, docs):
        pairs = [(query, doc.page_content) for doc in docs]
        scores = model.predict(pairs)

        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[:3]]