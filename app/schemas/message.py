from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str
    sender_id: int
    receiver_id: int

class MessageCreate(MessageBase):
    pass

class MessageUpdate(MessageBase):
    pass

class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True
