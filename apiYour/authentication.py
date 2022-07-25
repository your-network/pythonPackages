import os

def setAuthenticationHeader(YOUR_API_TOKEN: str) -> None:
    os.environ["YOUR_API_TOKEN"] = YOUR_API_TOKEN
