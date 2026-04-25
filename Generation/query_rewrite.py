def rewrite_query(llm, query: str) -> str:
    prompt = f"""
Rewrite the query for better semantic retrieval.

Rules:
- Keep meaning same
- Do NOT generate SQL/code
- Make it concise

Query: {query}
Improved:
"""
    return llm.invoke(prompt).content.strip()