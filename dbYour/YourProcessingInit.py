from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ProcessingDB:

    def __init__(self, SQLALCHEMY_DATABASE_URI):
        from .YourProcessingModels import Base
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
        Base.metadata.create_all(self.engine)

    def startSession(self):
        self.Session = sessionmaker(autocommit=True, autoflush=True, bind=self.engine)
        return self.session

    def closeSession(self,session):
        session.close()

    def closeConnection(self):
        self.engine.dispose()