from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relationships
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.recipient_id", back_populates="recipient")
    notifications = relationship("Notification", back_populates="user")
    contacts_as_user = relationship("Contact", foreign_keys="Contact.user_id", back_populates="user")
    contacts_as_contact = relationship("Contact", foreign_keys="Contact.contact_user_id", back_populates="contact_user")

class Contact(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="contacts_as_user")
    contact_user = relationship("User", foreign_keys=[contact_user_id], back_populates="contacts_as_contact")

class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.conversation_id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")
    conversation = relationship("Conversation", back_populates="messages")

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notifications")