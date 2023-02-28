import redis

def getRedisPool():
    print(f"Creating 1000 connection, aleksei wants to see this")
    pool = redis.ConnectionPool(host="localhost",
                                     port=6379,
                                     db=0,
                                     max_connections=10000)
    return pool

class RedisClient:
    def __init__(self, pool):
        self.pool = pool

    def getConnection(self):
        self.conn = redis.Redis(connection_pool=self.pool,
                                socket_timeout=300)
        return self.conn

    def closeConnection(self):
        self.conn.close()
        del self.conn
