from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


def db_connect(connect_string):
    return create_engine(connect_string)


def create_deals_table(engine):
    Base.metadata.create_all(engine)


class Packages(Base):
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    version = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=True)
    description = Column(String(500), nullable=False)
    maintainer = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    bugreport = Column(String(250), nullable=False)


class Imports(Base):
    __tablename__ = 'imports'
    id = Column(Integer, primary_key=True, nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    name = Column(String(250), nullable=False)
    version = Column(String(250), nullable=False)


class Suggests(Base):
    __tablename__ = 'suggests'
    id = Column(Integer, primary_key=True, nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    name = Column(String(250), nullable=False)
    version = Column(String(250), nullable=False)


class Exports(Base):
    __tablename__ = 'exports'
    id = Column(Integer, primary_key=True, nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    name = Column(String(250), nullable=False)


def setup_db(connect_string):
    engine = db_connect(connect_string)
    create_deals_table(engine)
