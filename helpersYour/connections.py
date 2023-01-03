import urllib3

class HTTPConnections:

    def openHTTPPool(self,
                 maxsize: int = 100,
                 num_pools: int = 10):

        self.http_pool = urllib3.PoolManager(num_pools=num_pools,
                                             maxsize=maxsize,
                                             timeout=60,
                                             retries=urllib3.util.retry.Retry(15))

        return self.http_pool

    def openHTTPConnection(self,
                           host: str,
                           maxsize: int = 100):

        self.http_connection = urllib3.HTTPConnectionPool(host, maxsize=maxsize)

        return self.http_connection

    def clearPool(self):
        self.http_pool.clear()
