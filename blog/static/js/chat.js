function sendMessage() {
    const url = document.getElementById('send-button').getAttribute('data-url');  
    const messageBox = document.getElementById("user-message");
    const message = messageBox.value;

    if (message.trim() === "") return;  // Ignore empty messages

    // Display user's message
    const chatBox = document.getElementById("chat-box");
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "chat-message user-message";
    userMessageDiv.textContent = message;
    chatBox.appendChild(userMessageDiv);

    // Clear the input
    messageBox.value = "";

    // Send message to Django backend
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            "message": message
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot's response
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "chat-message bot-message";
        botMessageDiv.textContent = data.bot_response;
        chatBox.appendChild(botMessageDiv);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

function addDeleteButton(messageDiv) {
const deleteButton = document.createElement("span");
deleteButton.className = "delete-button";
deleteButton.textContent = "x";
deleteButton.onclick = () => {
   
    messageDiv.style.animation = "fadeOut 0.3s ease";
    messageDiv.addEventListener("animationend", () => {
        messageDiv.remove();
    });
};
messageDiv.appendChild(deleteButton);
}





document.querySelectorAll('#favoritesOffcanvas .list-group-item a').forEach(link => {
    link.addEventListener('click', (e) => {
        console.log("Link clicked:", e.target);
    });
});
