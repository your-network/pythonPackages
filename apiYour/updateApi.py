import os
import requests
import json
from datetime import datetime
from helpersYour.logging import logging_error_message


def updateCategory(payload):
    r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        print(f"Update Call Success, category id: {payload.get('categoryId')}")
        return 200
    else:
        logging_error_message("update", "Update Category get all", payload, r.text, r.status_code)
