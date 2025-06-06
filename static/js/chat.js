// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const voiceToggle = document.getElementById('voice-toggle');
const clearChat = document.getElementById('clear-chat');
const themeToggle = document.getElementById('theme-toggle');
const emojiButton = document.getElementById('emoji-button');
const loadingOverlay = document.querySelector('.loading-overlay');
const voiceRecordingIndicator = document.querySelector('.voice-recording-indicator');
const sourcesModal = document.getElementById('sources-modal');
const sourcesList = document.getElementById('sources-list');
const closeModal = document.querySelector('.close-modal');

// State
let conversationId = null;
let isRecording = false;
let recognition = null;
let isDarkMode = false;

// Theme toggle
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}

// Load saved theme
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        isDarkMode = savedTheme === 'dark';
        document.body.setAttribute('data-theme', savedTheme);
        themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    }
}

// Emoji picker
function initEmojiPicker() {
    const picker = new EmojiButton({
        position: 'top-start',
        theme: isDarkMode ? 'dark' : 'light'
    });

    picker.on('emoji', emoji => {
        userInput.value += emoji;
        userInput.focus();
    });

    emojiButton.addEventListener('click', () => {
        picker.togglePicker(emojiButton);
    });
}

// Initialize speech recognition
function initializeSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    
    if (SpeechRecognition) {
        console.log('Speech recognition is supported');
        recognition = new SpeechRecognition();
        recognition.continuous = true;  // Keep recording
        recognition.interimResults = true;  // Get results as user speaks
        recognition.lang = 'en-US';

        let finalTranscript = '';

        recognition.onstart = () => {
            console.log('Speech recognition started');
            isRecording = true;
            voiceRecordingIndicator.style.display = 'flex';
            voiceToggle.classList.add('recording');
            finalTranscript = ''; // Reset transcript when starting new recording
        };

        recognition.onend = () => {
            console.log('Speech recognition ended');
            if (isRecording) {
                // If still recording (not manually stopped), restart
                recognition.start();
            } else {
                voiceRecordingIndicator.style.display = 'none';
                voiceToggle.classList.remove('recording');
                // Only send message if there's content
                if (finalTranscript.trim()) {
                    userInput.value = finalTranscript;
                    handleSendMessage();
                }
            }
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Show current transcription in input field
            userInput.value = finalTranscript + interimTranscript;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error !== 'no-speech') {
                alert(`Speech recognition error: ${event.error}. Please make sure your microphone is connected and you've granted permission to use it.`);
                isRecording = false;
                voiceRecordingIndicator.style.display = 'none';
                voiceToggle.classList.remove('recording');
            }
        };

        return true;
    }
    console.error('Speech recognition is not supported in this browser');
    return false;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadSavedTheme();
    userInput.focus();
    
    // Load emoji picker script
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@joeattardi/emoji-button@3.1.1/dist/index.min.js';
    script.onload = initEmojiPicker;
    document.head.appendChild(script);
    
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    // Initialize speech recognition
    if (!initializeSpeechRecognition()) {
        voiceToggle.style.display = 'none';
        console.log('Speech recognition not supported in this browser');
    }
});

themeToggle.addEventListener('click', toggleTheme);
sendButton.addEventListener('click', handleSendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
    }
});

voiceToggle.addEventListener('click', toggleVoiceInput);
clearChat.addEventListener('click', clearChatHistory);
closeModal.addEventListener('click', () => sourcesModal.style.display = 'none');

// Handle sending messages
async function handleSendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat with timestamp
    appendMessage(message, 'user', [], new Date());
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Show loading indicator
    loadingOverlay.style.display = 'flex';
    
    try {
        const response = await sendMessageToServer(message);
        appendMessage(response.response, 'bot', response.sources, new Date());
        conversationId = response.conversation_id;
    } catch (error) {
        appendMessage('Sorry, there was an error processing your message. Please try again.', 'bot', [], new Date());
        console.error('Error:', error);
    }
    
    loadingOverlay.style.display = 'none';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message to server
async function sendMessageToServer(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message,
            conversation_id: conversationId
        })
    });
    
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    
    return response.json();
}

// Append message to chat
function appendMessage(message, sender, sources = [], timestamp = new Date()) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const headerDiv = document.createElement('div');
    headerDiv.className = 'message-header';
    
    if (sender === 'bot') {
        headerDiv.innerHTML = '<i class="fas fa-robot"></i>';
    } else {
        headerDiv.innerHTML = '<i class="fas fa-user"></i>';
    }
    
    const time = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    headerDiv.innerHTML += `<span class="timestamp">${time}</span>`;
    
    contentDiv.appendChild(headerDiv);
    
    const paragraph = document.createElement('p');
    paragraph.textContent = message;
    contentDiv.appendChild(paragraph);
    
    if (sources && sources.length > 0) {
        const sourcesLink = document.createElement('div');
        sourcesLink.className = 'sources';
        sourcesLink.textContent = 'View Sources';
        sourcesLink.onclick = () => showSources(sources);
        contentDiv.appendChild(sourcesLink);
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
}

// Show sources in modal
function showSources(sources) {
    sourcesList.innerHTML = sources.map(source => `
        <div style="margin-bottom: 10px;">
            <a href="${source.url}" target="_blank">${source.title}</a>
            <p style="font-size: 0.9em; color: #666;">${source.type}</p>
        </div>
    `).join('');
    
    sourcesModal.style.display = 'flex';
}

// Voice input handling
function toggleVoiceInput() {
    if (!recognition) {
        alert('Speech recognition is not supported in your browser. Please try using Chrome, Edge, or another modern browser.');
        voiceToggle.style.display = 'none';
        return;
    }

    try {
        if (!isRecording) {
            // Request microphone permission before starting
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(() => {
                    console.log('Starting speech recognition...');
                    recognition.start();
                })
                .catch(error => {
                    console.error('Microphone access error:', error);
                    alert('Unable to access microphone. Please make sure you have granted microphone permissions.');
                });
        } else {
            console.log('Stopping speech recognition...');
            isRecording = false;  // Set this before stopping to prevent auto-restart
            recognition.stop();
        }
    } catch (error) {
        console.error('Speech recognition error:', error);
        alert('Error with speech recognition. Please try again.');
        isRecording = false;
        voiceRecordingIndicator.style.display = 'none';
        voiceToggle.classList.remove('recording');
    }
}

// Clear chat history
function clearChatHistory() {
    chatMessages.innerHTML = `
        <div class="message bot">
            <div class="message-content">
                <p>Hello! I'm your AI assistant. I can help you with information on any topic. What would you like to know?</p>
            </div>
        </div>
    `;
    conversationId = null;
} 