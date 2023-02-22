import os
from loggingYour.localLogging import LocalLogger

def removeProductMedia(connection: object,
                       media: str,
                       productId: str,
                       logger: LocalLogger = None) -> bool:

    ## logging
    if logger and os.environ.get('DEBUG') == 'DEBUG':
        log_message = {"topic": f"delete media from product",
                       "function": "removeProductMedia",
                       "endpoint": "/Product/{productId}/Media/{mediaId}",
                       "productId": productId,
                       "mediaId": media}
        logger.createDebugLog(message=log_message)

    ## request variables
    try:
        ## process request from connection pool
        r = connection.request(method="DELETE",
                               url=f"{os.environ['YOUR_API_URL']}/Product/{productId}/Media/{media}",
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        r.close()
        if response_code == 200:
            return True
        else:
            return False

    except Exception as e:
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error deleting media from product",
                           "function": "removeProductMedia",
                           "endpoint": "/Product/{productId}/Media/{mediaId}",
                           "productId": productId,
                           "mediaId": media,
                           "error": str(e)}
            logger.createErrorLog(message=log_message)

        return False


def removeCategoryMedia(media: str,
                        categoryId: int,
                        connection: object,
                        logger: LocalLogger = None) -> bool:

    ## logging
    if logger and os.environ.get('DEBUG') == 'DEBUG':
        log_message = {"topic": f"delete media from category",
                       "function": "removeCategoryMedia",
                       "endpoint": "/Category/{categoryId}/Media/{mediaId}",
                       "categoryId": categoryId,
                       "mediaId": media}
        logger.createDebugLog(message=log_message)

    ## request variables
    try:
        ## process request from connection pool
        r = connection.request(method="DELETE",
                               url=f"{os.environ['YOUR_API_URL']}/Category/{categoryId}/Media/{media}",
                               headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"],
                                        'Content-Type': 'application/json'})

        response_code = r.status
        r.close()
        if response_code == 200:
            return True
        else:
            return False

    except Exception as e:
        ## logging
        if logger and os.environ.get('DEBUG') == 'DEBUG':
            log_message = {"topic": f"Error deleting media from product",
                           "function": "removeCategoryMedia",
                           "endpoint": "/Category/{categoryId}/Media/{mediaId}",
                           "categoryId": categoryId,
                           "mediaId": media,
                           "error": str(e)}
            logger.createErrorLog(message=log_message)

        return False