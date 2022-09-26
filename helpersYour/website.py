
def getPageMetaData(url: str) -> dict:
    import requests
    from bs4 import BeautifulSoup
    import json

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, features="lxml")

    page_data = {}

    ## try via structured data schema.org
    scripts = soup.find_all('script', [])
    for script in scripts:
        if len(script.contents) > 0:
            contents = script.contents[0].strip()
            if 'schema.org' in contents:
                json_contents = json.loads(contents)

                page_data.update({'title': json_contents.get('name'),
                                  'description': json_contents.get('description'),
                                  'author': json_contents.get('creator'),
                                  'image': json_contents.get('image')})
    if page_data:
        return page_data

    else:
        ## via meta data
        page_data.update({'title': soup.title.string})
        meta = soup.find_all('meta')

        for tag in meta:
            if 'name' in tag.attrs.keys():
                if 'author' in tag.attrs['name'].strip().lower():
                    page_data.update({'author': tag.attrs['content'].strip()})
                if 'description' in tag.attrs['name'].strip().lower():
                    page_data.update({'description': tag.attrs['content'].strip()})
                if 'image' in tag.attrs['name'].strip().lower():
                    page_data.update({'image': tag.attrs['content'].strip()})

            elif 'property' in tag.attrs.keys():
                if 'image' in tag.attrs['property'].strip().lower():
                    page_data.update({'image': tag.attrs['content'].strip()})

        return page_data
