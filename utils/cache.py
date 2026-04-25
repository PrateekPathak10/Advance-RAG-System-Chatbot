from cachetools import TTLCache

cache= TTLCache(maxsize=100, ttl=300)

def get_cached(query):
    return cache.get(query)

def set_cache(query, response):
    cache[query]= response