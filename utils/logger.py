import logging

logging.basicConfig(level=logging.INFO)

def log_query(query):
    logging.info(f"Query: {query}")