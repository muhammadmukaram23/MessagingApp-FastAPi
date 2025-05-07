-- Create database if not exists
CREATE DATABASE IF NOT EXISTS messaging_system;
USE messaging_system;

-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    INDEX idx_email (email)
);

-- Create Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    contact_user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (contact_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255)
);

-- Create Messages table
CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    conversation_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- Create Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Insert some initial data
INSERT INTO users (username, email) VALUES 
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('bob_johnson', 'bob@example.com');

INSERT INTO contacts (user_id, contact_user_id) VALUES 
(1, 2),
(1, 3),
(2, 1),
(2, 3);

INSERT INTO conversations (subject) VALUES 
('Project Discussion'),
('Weekend Plans'),
('Meeting Notes');

INSERT INTO messages (sender_id, recipient_id, conversation_id, content) VALUES 
(1, 2, 1, 'Hi Jane, how is the project coming along?'),
(2, 1, 1, 'It''s going well! I''ll send you the updates tomorrow.'),
(1, 3, 2, 'Hey Bob, any plans for the weekend?'),
(3, 1, 2, 'Not yet, do you have something in mind?'),
(2, 3, 3, 'Here are the notes from our meeting today.');

INSERT INTO notifications (user_id, content) VALUES 
(1, 'You have 2 new messages'),
(2, 'Jane sent you a message'),
(3, 'John added you as a contact');