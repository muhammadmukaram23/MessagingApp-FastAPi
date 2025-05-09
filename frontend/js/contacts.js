class Contacts {
    constructor() {
        this.contacts = [];
        this.currentContact = null;
        this.apiBaseUrl = 'http://127.0.0.1:8001';
        this.pollInterval = null;
    }

    async loadContacts() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/${auth.userId}/contacts`, {
                headers: auth.getAuthHeader()
            });

            if (!response.ok) {
                throw new Error('Failed to load contacts');
            }

            const contactsRaw = await response.json();
            // Fetch user details for each contact
            this.contacts = await Promise.all(
                contactsRaw.map(async (contact) => {
                    // The contact_user_id is the other user
                    const userId = contact.contact_user_id;
                    try {
                        const userRes = await fetch(`${this.apiBaseUrl}/users/${userId}`, {
                            headers: auth.getAuthHeader()
                        });
                        if (userRes.ok) {
                            const user = await userRes.json();
                            return {
                                ...contact,
                                username: user.username,
                                email: user.email,
                                user_id: user.user_id
                            };
                        }
                    } catch (e) {}
                    // fallback if user fetch fails
                    return {
                        ...contact,
                        username: 'Unknown',
                        email: 'Unknown',
                        user_id: userId
                    };
                })
            );
            this.renderContacts();
        } catch (error) {
            console.error('Error loading contacts:', error);
        }
    }

    async addContact(contactUserId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/contacts/`, {
                method: 'POST',
                headers: {
                    ...auth.getAuthHeader(),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: auth.userId,
                    contact_user_id: contactUserId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add contact');
            }

            await this.loadContacts();
            return true;
        } catch (error) {
            console.error('Error adding contact:', error);
            return false;
        }
    }

    renderContacts() {
        const contactsList = document.getElementById('contactsList');
        contactsList.innerHTML = '';

        this.contacts.forEach(contact => {
            const contactElement = document.createElement('div');
            contactElement.className = 'contact-item';
            contactElement.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="flex-grow-1">
                        <h6 class="mb-0">${contact.username || 'Unknown'}</h6>
                        <small class="text-muted">${contact.email || 'Unknown'}</small>
                    </div>
                </div>
            `;

            contactElement.addEventListener('click', () => {
                this.selectContact(contact);
            });

            contactsList.appendChild(contactElement);
        });
    }

    selectContact(contact) {
        this.currentContact = contact;
        // Update UI
        document.getElementById('currentChat').textContent = contact.username;
        // Remove active class from all contacts
        document.querySelectorAll('.contact-item').forEach(item => {
            item.classList.remove('active');
        });
        // Add active class to selected contact
        event.currentTarget.classList.add('active');
        // Load messages for this contact
        messages.loadMessages(contact.user_id);
    }

    startPolling() {
        if (this.pollInterval) clearInterval(this.pollInterval);
        this.pollInterval = setInterval(() => {
            this.loadContacts();
        }, 5000); // Poll every 5 seconds
    }
}

// Initialize contacts
const contacts = new Contacts(); 