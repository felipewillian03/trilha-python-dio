from pydantic import BaseModel

from datetime import datetime

class PostOut(BaseModel):
    title: str
    author: str
    date: datetime