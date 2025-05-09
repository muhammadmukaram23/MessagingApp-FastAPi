from fastapi import FastAPI, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import get_db
from auth import verify_token   # for verfication token auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Messaging System API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Login endpoint
@app.post("/login/", tags=["Authentication"])
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.verify_user_credentials(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user_id": user.user_id, "username": user.username, "email": user.email}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Messaging System API"}

# User endpoints (only GET with email filter and GET by id)
@app.get("/users/", response_model=List[schemas.User],tags=["Users"],dependencies=[Depends(verify_token)])
def read_users(skip: int = 0, limit: int = 100, email: str = None, db: Session = Depends(get_db)):
    if email:
        user = crud.get_user_by_email(db, email=email)
        return [user] if user else []
    return []  # Only allow email filter

@app.get("/users/{user_id}", response_model=schemas.User,tags=["Users"],dependencies=[Depends(verify_token)])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Contacts endpoints (only POST and GET by user)
@app.post("/contacts/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED,tags=["Contacts"],dependencies=[Depends(verify_token)])
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/users/{user_id}/contacts", response_model=List[schemas.Contact],tags=["Contacts"],dependencies=[Depends(verify_token)])
def read_user_contacts(user_id: int, db: Session = Depends(get_db)):
    contacts = crud.get_user_contacts(db, user_id=user_id)
    return contacts

# Message endpoints (only POST and GET between two users)
@app.post("/messages/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED, tags=["Messages"], dependencies=[Depends(verify_token)])
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    # Create the message
    msg = crud.create_message(db=db, message=message)
    # Auto-add contacts in both directions if not already present
    from models import Contact
    if not db.query(Contact).filter_by(user_id=message.sender_id, contact_user_id=message.recipient_id).first():
        db.add(Contact(user_id=message.sender_id, contact_user_id=message.recipient_id))
    if not db.query(Contact).filter_by(user_id=message.recipient_id, contact_user_id=message.sender_id).first():
        db.add(Contact(user_id=message.recipient_id, contact_user_id=message.sender_id))
    db.commit()
    return msg

@app.get("/messages/between/{user1_id}/{user2_id}", response_model=List[schemas.Message], tags=["Messages"], dependencies=[Depends(verify_token)])
def get_messages_between_users(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    messages = crud.get_messages_between_users(db, user1_id, user2_id)
    return messages

# Notification endpoints (optional, keep if used by frontend)
@app.post("/notifications/", response_model=schemas.Notification, status_code=status.HTTP_201_CREATED,tags=["Notification"],dependencies=[Depends(verify_token)])
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification)

@app.get("/notifications/", response_model=List[schemas.Notification],tags=["Notification"],dependencies=[Depends(verify_token)])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, skip=skip, limit=limit)
    return notifications

@app.get("/users/{user_id}/notifications", response_model=List[schemas.Notification],tags=["Notification"],dependencies=[Depends(verify_token)])
def read_user_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = crud.get_user_notifications(db, user_id=user_id)
    return notifications

@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Notification"],dependencies=[Depends(verify_token)])
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    crud.delete_notification(db=db, notification_id=notification_id)
    return {"detail": "Notification deleted successfully"}