from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

# Contact schemas
class ContactBase(BaseModel):
    user_id: int
    contact_user_id: int

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    contact_id: int

    class Config:
        orm_mode = True

# Conversation schemas
class ConversationBase(BaseModel):
    subject: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    conversation_id: int

    class Config:
        orm_mode = True

# Message schemas
class MessageBase(BaseModel):
    sender_id: int
    recipient_id: int
    conversation_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Notification schemas
class NotificationBase(BaseModel):
    user_id: int
    content: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: int
    timestamp: datetime

    class Config:
        orm_mode = True