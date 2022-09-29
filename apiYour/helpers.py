def fillterCategoryPurpose(categories: list,
                           purpose: int) -> list:
    filter_list = []

    for category in categories:
        if category['purpose'] == purpose:
            filter_list.append(category)

    return filter_list

def getApiRequestsSession(endpoints: list = ["https://"]) -> object:
    import requests
    from requests.adapters import HTTPAdapter
    # To make sure we can use the requests session in the threadpool we
    # need to make sure that the connection pool can block. Otherwise it
    # will raise when it runs out of connections and the threads will be
    # terminated.
    requests_session = requests.Session()

    for endpoint in endpoints:
        requests_session.mount(endpoint, HTTPAdapter(
            pool_connections=10, pool_maxsize=1000, max_retries=5,
            pool_block=True))

    return requests_session