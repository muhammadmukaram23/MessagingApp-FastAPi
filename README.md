# Messaging System API

A FastAPI application for a messaging system with MySQL database support.

## System Overview

This API implements a messaging system with the following entities:

- **Users**: People who can send and receive messages
- **Contacts**: Connections between users
- **Conversations**: Thread of messages between users
- **Messages**: Individual communications sent between users
- **Notifications**: System alerts for users

## Database Schema

The database schema follows this structure:

- **User**
  - UserID (PK)
  - Username
  - Email

- **Contact**
  - ContactID (PK)
  - UserID (FK)
  - ContactUserID (FK)

- **Conversation**
  - ConversationID (PK)
  - Subject

- **Message**
  - MessageID (PK)
  - SenderID (FK)
  - RecipientID (FK)
  - ConversationID (FK)
  - Content
  - Timestamp

- **Notification**
  - NotificationID (PK)
  - UserID (FK)
  - Content
  - Timestamp

## API Endpoints

### User Endpoints

- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

### Contact Endpoints

- `POST /contacts/` - Create a new contact
- `GET /contacts/` - Get all contacts
- `GET /contacts/{contact_id}` - Get a specific contact
- `GET /users/{user_id}/contacts` - Get all contacts for a user
- `DELETE /contacts/{contact_id}` - Delete a contact

### Conversation Endpoints

- `POST /conversations/` - Create a new conversation
- `GET /conversations/` - Get all conversations
- `GET /conversations/{conversation_id}` - Get a specific conversation
- `GET /users/{user_id}/conversations` - Get all conversations for a user
- `DELETE /conversations/{conversation_id}` - Delete a conversation

### Message Endpoints

- `POST /messages/` - Create a new message
- `GET /messages/` - Get all messages
- `GET /messages/{message_id}` - Get a specific message
- `GET /conversations/{conversation_id}/messages` - Get all messages in a conversation
- `DELETE /messages/{message_id}` - Delete a message

### Notification Endpoints

- `POST /notifications/` - Create a new notification
- `GET /notifications/` - Get all notifications
- `GET /notifications/{notification_id}` - Get a specific notification
- `GET /users/{user_id}/notifications` - Get all notifications for a user
- `DELETE /notifications/{notification_id}` - Delete a notification

## Setup and Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Docker and Docker Compose (optional)

### Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/messaging-system-api.git
   cd messaging-system-api
   ```

2. Set up environment variables by creating a `.env` file (see `.env.example`):
   ```
   DATABASE_URL=mysql+pymysql://user:password@localhost/messaging_system
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running with Docker

The easiest way to start the application is using Docker Compose:

```bash
docker-compose up -d
```

This will:
1. Start a MySQL database container
2. Initialize the database with the schema and sample data
3. Start the FastAPI application on port 8000

### Running without Docker

1. Make sure MySQL is running and create the database:
   ```bash
   mysql -u root -p < init.sql
   ```

2. Start the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the application is running, you can access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Access the API using tools like curl, Postman, or directly through the Swagger UI.