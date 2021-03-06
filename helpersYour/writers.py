import json
import uuid
import itertools

def write_file_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)

def appending_data_json(data,file_name, dic_level):
    with open(file_name, 'r') as file:
        file_data = json.load(file)
    file_data.get(dic_level,[]).append(data)
    with open(file_name, "w") as file:
        json.dump(file_data, file)

def generateUUID():
    return uuid.uuid4().hex

def _batch_iter(n, iterable):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch