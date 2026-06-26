from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    title: str
    salary: int

class JobUpdate(BaseModel):
    title: Optional[str] = None
    salary: Optional[int] = None