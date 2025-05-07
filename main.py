from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import get_db

app = FastAPI(title="Messaging System API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Messaging System API"}

# User endpoints
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return {"detail": "User deleted successfully"}

# Contact endpoints
@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/users/{user_id}/contacts", response_model=List[schemas.Contact])
def read_user_contacts(user_id: int, db: Session = Depends(get_db)):
    contacts = crud.get_user_contacts(db, user_id=user_id)
    return contacts

@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db=db, contact_id=contact_id)
    return {"detail": "Contact deleted successfully"}

# Conversation endpoints
@app.post("/conversations/", response_model=schemas.Conversation, status_code=status.HTTP_201_CREATED)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    return crud.create_conversation(db=db, conversation=conversation)

@app.get("/conversations/", response_model=List[schemas.Conversation])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = crud.get_conversations(db, skip=skip, limit=limit)
    return conversations

@app.get("/conversations/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = crud.get_conversation(db, conversation_id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@app.get("/users/{user_id}/conversations", response_model=List[schemas.Conversation])
def read_user_conversations(user_id: int, db: Session = Depends(get_db)):
    conversations = crud.get_user_conversations(db, user_id=user_id)
    return conversations

@app.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = crud.get_conversation(db, conversation_id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    crud.delete_conversation(db=db, conversation_id=conversation_id)
    return {"detail": "Conversation deleted successfully"}

# Message endpoints
@app.post("/messages/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/messages/", response_model=List[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

@app.get("/messages/{message_id}", response_model=schemas.Message)
def read_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.get("/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def read_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = crud.get_conversation_messages(db, conversation_id=conversation_id)
    return messages

@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    crud.delete_message(db=db, message_id=message_id)
    return {"detail": "Message deleted successfully"}

# Notification endpoints
@app.post("/notifications/", response_model=schemas.Notification, status_code=status.HTTP_201_CREATED)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification)

@app.get("/notifications/", response_model=List[schemas.Notification])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, skip=skip, limit=limit)
    return notifications

@app.get("/notifications/{notification_id}", response_model=schemas.Notification)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@app.get("/users/{user_id}/notifications", response_model=List[schemas.Notification])
def read_user_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = crud.get_user_notifications(db, user_id=user_id)
    return notifications

@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    crud.delete_notification(db=db, notification_id=notification_id)
    return {"detail": "Notification deleted successfully"}