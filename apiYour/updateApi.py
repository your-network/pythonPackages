import os
import requests
import json
# from loggingYour.logging import logging_error_message


def updateCategory(payload, category_id):
    r = requests.put(f"https://api.yourcontent.io/Category/{category_id}",
                      json=payload,
                      headers={'Authorization': 'Bearer ' + os.environ["YOUR_API_TOKEN"]})
    if r.status_code == 200:
        resp_data = json.loads(r.text).get('data')
        if resp_data:
            media = resp_data.get('duplicates')
            return media
    else:
        logging_error_message("update", "Update category", payload, r.text, r.status_code)
        return None, None
