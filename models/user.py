from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True)
    password = Column(String(128))
    role = Column(String(16))  # admin, editor, viewer
