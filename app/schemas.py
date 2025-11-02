from pydantic import BaseModel, Field
from typing import List

class KratongCreate(BaseModel):
    id: str = Field(..., description="unique id from client (Date.now().toString())")
    ownerName: str
    wishText: str
    shapeImg: str
    createdAt: int  # timestamp in ms from client

class KratongOut(BaseModel):
    id: str
    ownerName: str
    wishText: str
    shapeImg: str
    createdAt: int

    class Config:
        from_attributes = True

class KratongList(BaseModel):
    kratongs: List[KratongOut]
