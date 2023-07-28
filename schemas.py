from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str | None = None


class Blog(BlogBase):
    author_id: int


class BaseUser(BaseModel):
    name: str
    email: str
    is_active: bool | None = True


class User(BaseUser):
    password: str


class ShowUser(BaseUser):
    blogs: List[BlogBase] = []

    class ConfigDict:
        from_attributes = True


class ShowBlog(BlogBase):
    author: BaseUser

    class ConfigDict:
        from_attributes = True
