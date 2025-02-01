function sendMessage() {
    let inputField = document.getElementById('user-input');
    let message = inputField.value.trim();
    if (message === '') return;

    let chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="message user-message"><strong>You:</strong> ${message}</div>`;

    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Bot response:", data.answer);
        chatBox.innerHTML += `<div class="message bot-message"><strong>Bot:</strong> ${data.answer}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    inputField.value = '';
}

function fillInput(element) {
    document.getElementById('user-input').value = element.textContent;
}