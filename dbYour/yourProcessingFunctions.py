from sqlalchemy import exc
import json
from datetime import datetime

def unprocessedProductIds(products, session):
    from YourProcessingModels import productQueue
    try:
        ## upload to database
        objects = []
        for count, product in enumerate(products):
            import_data = productQueue(source=2,
                                       productId=product['Product_ID'],
                                       language='EN',
                                       valueJson=json.dumps(product),
                                       status=0,
                                       createdAt=datetime.now(),
                                       updatedAt=None)
            objects.append(import_data)
            if len(objects) % 10000 == 0:
                session.bulk_save_objects(objects)
                objects = []
        session.bulk_save_objects(objects)
        session.commit()
        print(f"Bulk import finished")
    except exc.SQLAlchemyError as e:
        print(e)

def unprocessedMedia(media, session):
    from YourProcessingModels import mediaQueue

    try:
        ## upload to database
        objects = []
        for count, entry in enumerate(media):
            import_data = mediaQueue(url=entry['url'],
                                     type=entry['contentType'],
                                     resolution=entry['resolution'],
                                     shA256=entry['shA256'],
                                     internalPath=entry['internalPath'],
                                     status=0,
                                     createdAt=datetime.now(),
                                     updatedAt=None)
            objects.append(import_data)
            if len(objects) % 10000 == 0:
                session.bulk_save_objects(objects)
                objects = []
        session.bulk_save_objects(objects)
        session.commit()
        print(f"Bulk media import finished")
    except exc.SQLAlchemyError as e:
        print(e)
