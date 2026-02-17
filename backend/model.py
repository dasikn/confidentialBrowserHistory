from pydantic import BaseModel
from datetime import datetime


class Website(BaseModel):
    url: str
    title: str
    html: str
    access_time: datetime


class SearchResult(BaseModel):
    text: str
    score: float | None
    url: str | None
    title: str | None
