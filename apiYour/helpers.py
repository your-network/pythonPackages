def fillterCategoryPurpose(categories: list,
                           purpose: int) -> list:
    filter_list = []

    for category in categories:
        if category['purpose'] == purpose:
            filter_list.append(category)

    return filter_list

def getApiRequestsSession(endpoint: str = None) -> object:
    import requests
    from requests.adapters import HTTPAdapter
    # To make sure we can use the requests session in the threadpool we
    # need to make sure that the connection pool can block. Otherwise it
    # will raise when it runs out of connections and the threads will be
    # terminated.
    requests_session = requests.Session()
    mount_url = "https://"
    if endpoint:
        mount_url = endpoint
    requests_session.mount(mount_url, HTTPAdapter(
        pool_connections=10, pool_maxsize=1000, max_retries=5,
        pool_block=True))

    return requests_session