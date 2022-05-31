from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ProcessingDB:

    def __init__(self, SQLALCHEMY_DATABASE_URI):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600)

        self.Session = sessionmaker(autocommit=True, autoflush=True, bind=self.engine)

    def startSession(self):
        from .YourProcessingModels import Base
        # 2 - generate database schema
        Base.metadata.create_all(self.engine)

        # 3 - create a new session
        self.session = self.Session()
        return self.session

    @staticmethod
    def closeSession(session,db):
        session.close()
        db.dispose()