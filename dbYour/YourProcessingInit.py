from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .YourProcessingModels import Base

class ProcessingDB:

    def __init__(self, SQLALCHEMY_DATABASE_URI):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
        Base.metadata.create_all(self.engine)

    def startSession(self):
        Session = sessionmaker(autocommit=True, autoflush=True, bind=self.engine)
        self.session = Session()
        return self.session

    def closeSession(self):
        self.session.flush()
        self.session.close()

    def closeConnection(self):
        self.engine.dispose()