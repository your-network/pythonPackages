import redis

class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RedisPool(metaclass=Singleton):

    def getPool(self):
        print(f"Creating 1000 connection, aleksei wants to see this")
        self.pool = redis.ConnectionPool(host="localhost",
                                         port=6379,
                                         db=0,
                                         max_connections=10000)
        return self.pool

class RedisClient(metaclass=Singleton):
    def connection(self, ConnectionPool):
        self.pool = ConnectionPool
        if not hasattr(self, '_conn'):
            self.getConnection()
        return self._conn

    def getConnection(self):
        self._conn = redis.Redis(connection_pool=self.pool,
                                 socket_timeout=300)

    def closeConnection(self):
        self._conn.close()
        del self._conn
