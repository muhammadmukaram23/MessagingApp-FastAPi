// Check if user is already logged in
document.addEventListener('DOMContentLoaded', () => {
    if (auth.isAuthenticated()) {
        auth.showMainApp();
        contacts.startPolling(); // Start real-time polling for contacts
    }
});

// Add logout button to the UI
const logoutButton = document.createElement('button');
logoutButton.className = 'btn btn-outline-danger btn-sm mt-2';
logoutButton.textContent = 'Logout';
logoutButton.addEventListener('click', () => {
    auth.logout();
});

document.querySelector('.user-profile').appendChild(logoutButton);

// Add search functionality for contacts
const searchInput = document.createElement('input');
searchInput.type = 'text';
searchInput.className = 'form-control mb-3';
searchInput.placeholder = 'Search contacts...';

searchInput.addEventListener('input', async (e) => {
    const searchTerm = e.target.value.trim();
    if (searchTerm) {
        try {
            const response = await fetch(`http://127.0.0.1:8001/users/?email=${searchTerm}`, {
                headers: auth.getAuthHeader()
            });

            if (!response.ok) {
                throw new Error('Failed to search users');
            }

            const users = await response.json();
            const contactsList = document.getElementById('contactsList');
            contactsList.innerHTML = '';

            users.forEach(user => {
                if (user.user_id !== auth.userId) {
                    const userElement = document.createElement('div');
                    userElement.className = 'contact-item';
                    userElement.innerHTML = `
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <h6 class="mb-0">${user.username}</h6>
                                <small class="text-muted">${user.email}</small>
                            </div>
                            <button class="btn btn-primary btn-sm add-contact" data-user-id="${user.user_id}">
                                Add Contact
                            </button>
                        </div>
                    `;

                    userElement.querySelector('.add-contact').addEventListener('click', async (e) => {
                        e.stopPropagation();
                        const userId = e.target.dataset.userId;
                        await contacts.addContact(userId);
                        searchInput.value = '';
                        contacts.loadContacts();
                    });

                    contactsList.appendChild(userElement);
                }
            });
        } catch (error) {
            console.error('Error searching users:', error);
        }
    } else {
        contacts.loadContacts();
    }
});

document.querySelector('.contacts-list').insertBefore(searchInput, document.getElementById('contactsList')); 