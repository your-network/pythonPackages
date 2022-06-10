from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class mediaQueue(Base):
    __tablename__ = 'mediaQueue'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    contentType = Column(String)
    resolution = Column(String)
    shA256 = Column(String)
    internalPath = Column(String)
    status = Column(Integer)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
    def __init__(self, **kwargs):
        super(mediaQueue, self).__init__(**kwargs)

class productQueue(Base):
    __tablename__ = 'productQueue'
    id = Column(Integer, primary_key=True)
    source = Column(Integer)
    productId = Column(Integer)
    language = Column(String)
    valueJson = Column(String, nullable=True)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(productQueue, self).__init__(**kwargs)

class categoryQueue(Base):
    __tablename__ = 'categoryQueue'
    id = Column(Integer, primary_key=True)
    source = Column(Integer)
    purpose = Column(Integer)
    categoryId = Column(String)
    language = Column(String)
    valueJson = Column(String, nullable=True)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(categoryQueue, self).__init__(**kwargs)

class relationQueue(Base):
    __tablename__ = 'relationQueue'
    id = Column(Integer, primary_key=True)
    relationType = Column(String)
    entityId = Column(String)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(relationQueue, self).__init__(**kwargs)

class latestUpdateDate(Base):
    __tablename__ = 'latestUpdateDate'
    type = Column(String, primary_key=True)
    source = Column(Integer)
    purpose = Column(Integer)
    updateDate = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(latestUpdateDate, self).__init__(**kwargs)
