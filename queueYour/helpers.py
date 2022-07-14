import json

class Utils:

    def __init__(self):
        pass

    def decoded_data_to_json(self,decoded_data):
        try:
            decoded_data = decoded_data.replace("'", '"')
            json_data = json.loads(decoded_data)
            return json_data
        except Exception as e:
            raise Exception('error while parsing json')

    def raw_data_to_utf(self,raw_data):
        try:
            decoded_data = raw_data.decode('utf8')
            return decoded_data
        except Exception as e:
            raise Exception('error converting to UTF')