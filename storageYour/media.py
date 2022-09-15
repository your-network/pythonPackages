
def imageFileS3BucketUpload(storageService: object,
                            content_bytes: object,
                            extension: str,
                            shA256: str,
                            msg_handler: object):
    import hashlib
    import traceback

    ## logging
    msg_handler.logStruct(
        topic=f"imageFileS3BucketUpload: file: {shA256}, to media bucket",
        level="DEBUG",
        labels={"function": "imageFileS3BucketUpload"})

    try:
        final_path = f"m/{shA256}.{extension}"

        ## upload object
        my_bucket = storageService.Bucket("yourcontent-dev")
        my_bucket.upload_fileobj(content_bytes,
                                 final_path,
                                 ExtraArgs={'ACL': "public-read"})

        ## logging
        msg_handler.logStruct(
            topic=f"imageFileS3BucketUpload: internal path: {final_path}, sha256: {shA256} object uploaded",
            level="DEBUG",
            labels={"function": "imageFileS3BucketUpload"})

        return True

    except:
        ## logging
        error = traceback.format_exc()
        msg_handler.logStruct(topic=f"imageFileS3BucketUpload: file: {shA256}, error",
                              error_message=str(error),
                              level="ERROR",
                              labels={"function": "imageFileS3BucketUpload"})
        return False


def mediaUrlS3BucketUpload(storageService: object, media_url: str, internal_path: str, msg_handler: object):
    from io import BytesIO
    import traceback
    import requests

    response = requests.get(media_url, timeout=15)

    ## logging
    msg_handler.logStruct(topic=f"mediaUrlS3BucketUpload: url: {media_url}, request made. Status code: {response.status_code}",
                          data=response.status_code,
                          level="DEBUG",
                          labels={"function": "mediaUrlS3BucketUpload"})

    if response.status_code == 200:
        try:
            bytes_content = BytesIO(response.content)
            bytes_content.seek(0)
            content_type = response.headers['Content-Type']

            ## upload details
            my_bucket = storageService.Bucket("yourcontent-dev")
            final_path = f"m{internal_path}"

            my_bucket.upload_fileobj(bytes_content,
                                     final_path,
                                     ExtraArgs={'ContentType': content_type, 'ACL': "public-read"})

            ## logging
            msg_handler.logStruct(topic=f"mediaUrlS3BucketUpload: media url: {media_url}, sha256: {internal_path} object uploaded",
                                  level="DEBUG",
                                  labels={"function": "uploadBytesMedia"})
            return True

        except:
            ## logging
            error = traceback.format_exc()
            msg_handler.logStruct(topic=f"mediaUrlS3BucketUpload: media url: {media_url}, error",
                                  error_message=str(error),
                                  level="ERROR",
                                  labels={"function": "uploadBytesMedia"})
            return False

    else:
        ## logging
        msg_handler.logStruct(
            topic=f"mediaUrlS3BucketUpload: url: {media_url}, request made. Status code: {response.status_code}",
            data=response.text,
            level="WARNING",
            labels={"function": "mediaUrlS3BucketUpload"})

        return False
