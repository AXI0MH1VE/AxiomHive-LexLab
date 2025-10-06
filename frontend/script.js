document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newChatBtn = document.getElementById('newChatBtn');

    let conversationId = null; // To manage conversation state with the backend

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'ai-message', 'typing-indicator');
        typingDiv.innerHTML = '<p>...</p>';
        chatHistory.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }

    function removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessage(message, 'user');
        userInput.value = '';
        sendBtn.disabled = true;
        userInput.style.height = 'auto';

        const typingIndicator = showTypingIndicator();

        try {
            const API_ENDPOINT = 'http://localhost:8000/chat/process'; 
            const userId = 'user_123';

            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    message: message,
                    conversation_id: conversationId,
                    metadata: {}
                }),
            });

            removeTypingIndicator(typingIndicator);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to get response from AI.');
            }

            const data = await response.json();
            addMessage(data.response, 'ai');

            if (data.conversation_id && !conversationId) {
                conversationId = data.conversation_id;
            }

        } catch (error) {
            console.error('Error sending message:', error);
            removeTypingIndicator(typingIndicator);
            addMessage(`Error: ${error.message || 'Could not connect to the AI.'}`, 'ai');
        } finally {
            sendBtn.disabled = false;
            scrollToBottom();
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    newChatBtn.addEventListener('click', () => {
        chatHistory.innerHTML = `
            <div class="message system-message">
                <p>Welcome to the Transcendent AI Chatbot. How can I assist you today?</p>
            </div>
        `;
        userInput.value = '';
        conversationId = null;
        scrollToBottom();
    });

    scrollToBottom();
});
