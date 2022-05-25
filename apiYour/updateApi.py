import os
import requests
import json
from datetime import datetime


def updateCategory(payload):
    r = requests.post('https://api.yourcontent.io/Category/CreateOrUpdate',
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
    if r.status_code == 200:
        print(f"Update Call Success, category id: {payload.get('categoryId')}")
        return 200
    else:
        print(f"Update Call failed. Response code: {r.status_code}, text: {r.text}")