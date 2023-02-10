from decouple import config
import os
import rootpath
abs_path = rootpath.detect()

## cache
from redis import Redis

redis = Redis(host="localhost",
              port=6379,
              db=0,
              decode_responses=True)

# Request variables
from helpersYour.connections import HTTPConnections
## connection pool
Connections = HTTPConnections()
connectionPool = Connections.openHTTPPool()

## queue pub sub
from queueYour.auth import QueueAuth
## pub/sub auth
queue = QueueAuth(f"./files/atomic-affinity-356010-c4893c67467b.json",
                  os.environ['GOOGLE_PROJECT_ID'])

## Variables
ACTIVE_LANGUAGES = ["en", "nl"]
## active categories
ACTIVE_CATEGORIES = []
with open(f"{abs_path}/files/activeCategoryList.txt") as f:
    for line in f.readlines():
        ACTIVE_CATEGORIES.append(int(line.strip()))