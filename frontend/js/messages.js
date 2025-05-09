class Messages {
    constructor() {
        this.messages = [];
        this.messageForm = document.getElementById('messageForm');
        this.messageInput = document.getElementById('messageInput');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.apiBaseUrl = 'http://127.0.0.1:8001';  // Updated API base URL
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
    }

    async loadMessages(contactId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/messages/between/${auth.userId}/${contactId}`, {
                headers: auth.getAuthHeader()
            });

            if (!response.ok) {
                throw new Error('Failed to load messages');
            }

            this.messages = await response.json();
            this.renderMessages();
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    async sendMessage() {
        if (!contacts.currentContact) {
            alert('Please select a contact first');
            return;
        }

        const content = this.messageInput.value.trim();
        if (!content) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/messages/`, {
                method: 'POST',
                headers: {
                    ...auth.getAuthHeader(),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sender_id: auth.userId,
                    recipient_id: contacts.currentContact.user_id,
                    content: content
                })
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            // Clear input
            this.messageInput.value = '';

            // Reload messages
            await this.loadMessages(contacts.currentContact.user_id);
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message');
        }
    }

    renderMessages() {
        this.messagesContainer.innerHTML = '';

        this.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${message.sender_id === auth.userId ? 'sent' : 'received'}`;
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = message.content;
            
            const messageTime = document.createElement('div');
            messageTime.className = 'message-time';
            messageTime.textContent = new Date(message.timestamp).toLocaleTimeString();
            
            messageElement.appendChild(messageContent);
            messageElement.appendChild(messageTime);
            
            this.messagesContainer.appendChild(messageElement);
        });

        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    // Poll for new messages
    startPolling() {
        setInterval(() => {
            if (contacts.currentContact) {
                this.loadMessages(contacts.currentContact.user_id);
            }
        }, 5000); // Poll every 5 seconds
    }
}

// Initialize messages
const messages = new Messages(); 