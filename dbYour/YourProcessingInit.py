
class ProcessingDB:
    from .settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO, WTF_CSRF_SECRET_KEY, SECRET_KEY

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=True)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def startSession(self):
        from .YourProcessingModels import Base
        # 2 - generate database schema
        Base.metadata.create_all(self.engine)

        # 3 - create a new session
        self.session = self.Session()
        return self.session

    def closeSession(self):
        self.session.close()
        self.engine.dispose()
