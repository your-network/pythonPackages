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
    productId = Column(String)
    language = Column(String)
    valueJson = Column(String, nullable=True)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(productQueue, self).__init__(**kwargs)

class productQueueCopy(Base):
    __tablename__ = 'productQueueCopy'
    id = Column(Integer, primary_key=True)
    source = Column(Integer)
    productId = Column(String)
    language = Column(String)
    valueJson = Column(String, nullable=True)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(productQueueCopy, self).__init__(**kwargs)

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

class brandQueue(Base):
    __tablename__ = 'brandQueue'
    id = Column(Integer, primary_key=True)
    source = Column(Integer)
    brandId = Column(String)
    valueJson = Column(String, nullable=True)
    status = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(brandQueue, self).__init__(**kwargs)

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

class references(Base):
    __tablename__ = 'references'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    source = Column(Integer)
    purpose = Column(Integer)
    externalId = Column(Integer)
    internalId = Column(Integer)
    createdAt = Column(DateTime, nullable=True)
    updatedAt = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(references, self).__init__(**kwargs)

class latestUpdateDate(Base):
    __tablename__ = 'latestUpdateDate'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    source = Column(Integer)
    purpose = Column(Integer)
    updateDate = Column(DateTime, nullable=True)
    def __init__(self, **kwargs):
        super(latestUpdateDate, self).__init__(**kwargs)
