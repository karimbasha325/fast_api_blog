from .database import Base
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(256))
    is_active = Column(Boolean, default=True)

    blogs = relationship("Blog", back_populates="author")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(32))
    body = Column(String(1000))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="blogs")
