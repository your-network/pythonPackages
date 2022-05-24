import requests
import json

API_KEY_AL = "pHMfRlA4Vt5HGHgw-LQkxyqJU5au9Yee"
REQUEST_URL = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY_AL}/getNFTsForCollection"
HEADERS = {
    "Accept": "application/json"
}

def getCollectionNFTs(contract_address):
    parameters = {'contractAddress': contract_address,
                  'withMetadata': 'true'}

    collection_nfts = []

    pagination = True
    page = 0
    while pagination:
        if page > 0:
            parameters.update({'startToken': next_page})

        response = requests.request("GET", REQUEST_URL,
                                    headers=HEADERS,
                                    params=parameters)
        data = json.loads(response.content)

        ## append collection
        collection_nfts = collection_nfts + data.get('nfts')
        print(f"Call success, nft list appended: {len(collection_nfts)}")
        next_page = data.get('nextToken')
        if next_page:
            page += 1
            continue
        else:
            break

    return collection_nfts