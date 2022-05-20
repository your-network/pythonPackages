STATUS = {'process': 0,
          'done': 1,
          'failed': 2}
SOURCE = {'Internal':1,
    'Icecat':2,
    'Bol':3,
    'Amazon':4,
    'Opensea':5,
    'Decentraland': 6,
    'Sandbox':7}

## dbYour sqlalchemy
SQLALCHEMY_DATABASE_URI = "mariadb+mariadbconnector://admin:CVTc6nR645jFraIll1NZ@oehoe-prod-master-01.crrprfk47ofc.eu-central-1.rds.amazonaws.com:3306/YourContentData"
WTF_CSRF_SECRET_KEY = '123456789987654321'
SECRET_KEY = '123456789987654321'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
