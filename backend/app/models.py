from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    facebook_id = Column(String, unique=True, index=True)
    name = Column(String)
    session_token = Column(String)
