import os

from redis import Redis, ConnectionPool

def getRedisPool(host: str,
                 password: str,
                 user:str = None):
    if user:
        pool = ConnectionPool(host=host,
                              port=6379,
                              db=0,
                              max_connections=10000,
                              username=user,
                              password=password,
                              decode_responses=True)
    else:
        pool = ConnectionPool(host=host,
                              port=6379,
                              db=0,
                              max_connections=10000,
                              password=password,
                              decode_responses=True)
    return pool

class RedisClient:
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def getConnection(self):
        self.conn = Redis(connection_pool=self.pool,
                          socket_timeout=300)
        return self.conn

    def closeConnection(self):
        self.conn.close()
        del self.conn
