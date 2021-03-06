import re
from gzip import GzipFile
from urllib.request import urlopen,HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener,install_opener
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import hashlib

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_digits(string):
    digits = re.findall(r'\d+', string)
    if len(digits) == 0:
        return None
    elif len(digits) > 1:
        return float(".".join(map(str,digits)))
    elif len(digits) == 1:
        return int(digits[0])

def remove_nulls(d):
    none_filtered = {k: v for k, v in d.items() if v is not None}
    return {k: v for k, v in none_filtered.items() if v != ''}

def remove_dic_none_values(dic):
    remove_fields = []
    for key,value in dic.items():
        if value is None and key is not None:
            remove_fields.append(key)
    final_dic = remove_dic_key(dic,remove_fields)
    return final_dic

def remove_dic_key(dic,keys):
    for remove in keys:
        try:
            del dic[remove]
        except:
            continue
    return dic

def rename_dic_key(dic={},naming=[]):
    for row in naming:
        old = row.get('old',None)
        new = row.get('new',None)
        if old:
            dic[new] = dic.pop(old)
    return dic

def open_xml_gz_url(request_url, file_path, auth=False, username=None, password=None):
    try:
        if auth:
            # create a password manager
            password_mgr = HTTPPasswordMgrWithDefaultRealm()

            # Add the username and password.
            # If we knew the realm, we could use it instead of None.
            password_mgr.add_password(None, request_url, username, password)

            handler = HTTPBasicAuthHandler(password_mgr)

            # create "opener" (OpenerDirector instance)
            opener = build_opener(handler)

            # use the opener to fetch a URL
            opener.open(request_url)
            opener.addheaders.append(("Accept-Encoding", "gzip"))
            # Install the opener.
            # Now all calls to urllib.request.urlopen use our opener.
            install_opener(opener)

            response = urlopen(request_url)
        else:
            response = urlopen(request_url)

        compressed_file = BytesIO(response.read())
        decompressed_file = GzipFile(fileobj=compressed_file)
        with open(file_path, 'wb') as outfile:
            outfile.write(decompressed_file.read())
        return True
    except Exception as e:
        print('Failed to download and unpack url: '+ str(e))
        return False

def image_details(image_url):
    response = requests.get(image_url)
    ## size
    im = Image.open(BytesIO(response.content))
    w, h = im.size
    ## hash
    Na = np.array(im).astype(np.uint16)
    sha256 = hashlib.sha256(Na.tobytes()).hexdigest()
    return w, h, sha256

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def str_to_bool(s):
    if s.lower() == 'true':
         return True
    elif s.lower() == 'false':
         return False
    else:
        print(s)
        raise ValueError

