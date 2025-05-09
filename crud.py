from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
import bcrypt

import models
import schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def verify_user_credentials(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    # Verify the password against the stored hash
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8')
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# Contact CRUD operations
def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_user_contacts(db: Session, user_id: int):
    return db.query(models.Contact).filter(models.Contact.user_id == user_id).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        user_id=contact.user_id,
        contact_user_id=contact.contact_user_id
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return db_contact

# Message CRUD operations
def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.message_id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()

def get_conversation_messages(db: Session, conversation_id: int):
    return db.query(models.Message)\
        .filter(models.Message.conversation_id == conversation_id)\
        .order_by(models.Message.timestamp)\
        .all()

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        sender_id=message.sender_id,
        recipient_id=message.recipient_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int):
    db_message = db.query(models.Message).filter(models.Message.message_id == message_id).first()
    db.delete(db_message)
    db.commit()
    return db_message

# Notification CRUD operations
def get_notification(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.notification_id == notification_id).first()

def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).offset(skip).limit(limit).all()

def get_user_notifications(db: Session, user_id: int):
    return db.query(models.Notification)\
        .filter(models.Notification.user_id == user_id)\
        .order_by(desc(models.Notification.timestamp))\
        .all()

def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(
        user_id=notification.user_id,
        content=notification.content
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int):
    db_notification = db.query(models.Notification).filter(models.Notification.notification_id == notification_id).first()
    db.delete(db_notification)
    db.commit()
    return db_notification

# Add function to get all messages between two users
def get_messages_between_users(db: Session, user1_id: int, user2_id: int):
    return db.query(models.Message).filter(
        ((models.Message.sender_id == user1_id) & (models.Message.recipient_id == user2_id)) |
        ((models.Message.sender_id == user2_id) & (models.Message.recipient_id == user1_id))
    ).order_by(models.Message.timestamp).all()