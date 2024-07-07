from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    content: str
    sender_id: int
    receiver_id: int
    image: Optional[bytes] = None  

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True
