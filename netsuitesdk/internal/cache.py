import redis
from zeep.cache import Base


class RedisCache(Base):
    """Simple in-memory caching using dict lookup with support for timeouts"""

    _cache = {}  # global cache, thread-safe by default

    def __init__(self, host, db, timeout=3600):
        self._timeout = timeout
        self._host = host
        self._db = db
        self._client = redis.Redis(host=host,
                                   port=6379,
                                   db=db)

    def add(self, url, content):
        if not isinstance(content, (str, bytes)):
            raise TypeError(
                "a bytes-like object is required, not {}".format(type(content).__name__)
            )
        self._client.set(url, content, timeout)

    def get(self, url):
        content = self._client.get(url)
        if content:
            return content
        return None
