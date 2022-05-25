import os

def setAuthenticationHeader(YOUR_API_TOKEN):
    os.environ["YOUR_API_HEADER"] = {'Authorization': 'Bearer ' + YOUR_API_TOKEN}
