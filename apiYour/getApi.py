import os
import requests
import json
from datetime import datetime

def getAllCategories():
    next_page = True
    page = 1
    categories = []
    while next_page:
        r = requests.get(f"https://api.yourcontent.io/Category/GetAll?resultsPerPage=100&page={page}",
                         headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_HEADER"]})
        if r.status_code == 200:
            result = json.loads(r.text)
            data = result.get('data')
            if len(data) > 0:
                categories = categories + data
                page += 1
            else:
                break
        else:
            print(f"Attribute create Error. Response text: {r.content}")
            break

    return categories