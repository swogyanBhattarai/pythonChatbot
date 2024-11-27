document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally
    let messageInput = document.getElementById('message-input');
    let message = messageInput.value;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams('message=' + message)
    })
    .then(response => response.json())
    .then(data => {
        let messagesDiv = document.getElementById('messages');

        // Create user message box
        let userMessageBox = document.createElement('div');
        userMessageBox.className = 'message-box user';
        userMessageBox.innerHTML = `<p>${data.user_input}</p>`;
        messagesDiv.appendChild(userMessageBox);

        // Create bot reply box
        let botMessageBox = document.createElement('div');
        botMessageBox.className = 'message-box bot';
        botMessageBox.innerHTML = `<p>${data.bot_reply}</p>`;
        messagesDiv.appendChild(botMessageBox);

        // Clear input
        messageInput.value = '';

        // Scroll to the bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
});
