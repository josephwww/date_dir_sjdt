from sqlalchemy import Column, String, Text, Enum, ForeignKey, JSON
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DBResource(Base):
    __tablename__ = 'db_resources'

    id = Column(CHAR(36), primary_key=True)
    resource_name = Column(String(100))
    resource_type = Column(Enum('Database', 'Table', 'System', name='resource_type'), nullable=False)
    extra = Column(JSON, nullable=True)


class DataDirectory(Base):
    __tablename__ = 'data_directories'

    id = Column(CHAR(36), primary_key=True)
    system_id = Column(CHAR(36), ForeignKey('db_resources.id'))
    db_id = Column(CHAR(36), ForeignKey('db_resources.id'))
    table_id = Column(CHAR(36), ForeignKey('db_resources.id'))
    entry_name = Column(String(255), nullable=False)
    comment = Column(Text)

    system = relationship('DBResource', foreign_keys=[system_id])
    database = relationship('DBResource', foreign_keys=[db_id])
    table = relationship('DBResource', foreign_keys=[table_id])
