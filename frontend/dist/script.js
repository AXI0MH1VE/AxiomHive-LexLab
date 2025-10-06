// Copied static script for packaged UI
document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newChatBtn = document.getElementById('newChatBtn');

    let conversationId = null;

    function scrollToBottom(){ chatHistory.scrollTop = chatHistory.scrollHeight }
    function addMessage(text, sender){ const messageDiv = document.createElement('div'); messageDiv.classList.add('message', `${sender}-message`); const p = document.createElement('p'); p.textContent = text; messageDiv.appendChild(p); chatHistory.appendChild(messageDiv); scrollToBottom() }

    async function sendMessage(){
        const message = userInput.value.trim(); if(!message) return; addMessage(message,'user'); userInput.value=''; sendBtn.disabled=true; const typing = document.createElement('div'); typing.className='message ai-message typing-indicator'; typing.innerHTML='<p>...</p>'; chatHistory.appendChild(typing);
        try{
            const res = await fetch('http://localhost:8000/chat/process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:'user_123',message:message,conversation_id:conversationId,metadata:{}})});
            chatHistory.removeChild(typing);
            if(!res.ok){ addMessage('Error: AI returned an error','ai'); }
            else{ const data = await res.json(); addMessage(data.response || '[no response]','ai'); }
        }catch(e){ chatHistory.removeChild(typing); addMessage('Error: Could not connect to AI','ai') }
        finally{ sendBtn.disabled=false; scrollToBottom() }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e)=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMessage() } });
    newChatBtn.addEventListener('click', ()=>{ chatHistory.innerHTML = `<div class="message system-message"><p>Welcome to the Transcendent AI Chatbot. How can I assist you today?</p></div>`; conversationId=null })
});
