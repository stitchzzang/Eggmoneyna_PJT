<template>
    <div class="chatbot-container">
        <div class="chat-messages">
            <div v-for="message in messages" :key="message.id" 
                 :class="['message-wrapper', message.sender === 'user' ? 'user-message' : 'ai-message']">
                <div class="message-bubble">
                    {{ message.text }}
                </div>
            </div>
        </div>
        <div class="chat-input-container">
            <input 
                type="text" 
                v-model="userInput" 
                @keyup.enter="sendMessage"
                placeholder="메시지를 입력하세요..."
                class="chat-input"
            >
            <button @click="sendMessage" class="send-button">
                전송
            </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            userInput: '',
            messages: []
        };
    },
    methods: {
        async sendMessage() {
            const userMessage = this.userInput.trim();
            if (!userMessage) return;

            this.addMessage('user', userMessage);

            const aiResponse = await this.getAiResponse(userMessage);
            this.addMessage('ai', aiResponse);

            this.userInput = '';
        },
        addMessage(sender, text) {
            this.messages.push({id: Date.now(), sender, text});
        },
        async getAiResponse(message) {
            try {
                const apiKey = import.meta.env.VITE_AI_API_KEY;
                
                const response = await axios.post('https://api.openai.com/v1/chat/completions', {
                    model: "gpt-4o-mini",
                    messages: [
                        {'role': "user", 'content': message},
                        {"role": "system", "content": "You are a helpful assistant."},],
                    max_tokens: 150,
                    temperature: 0.7
                }, {
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                return response.data.choices[0].message.content.trim();
            } catch (error) {
                console.error('AI 응답 오류:', error);
                if (error.response?.status === 429) {
                    return '죄송합니다. 잠시 후 다시 시도해주세요.';
                }
                return `오류가 발생했습니다: ${error.message}`;
            }
        }
    }
}
</script>

<style scoped>
.chatbot-container {
    width: 320px;
    height: 450px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
}

.message-wrapper {
    margin: 8px 0;
    display: flex;
}

.user-message {
    justify-content: flex-end;
}

.ai-message {
    justify-content: flex-start;
}

.message-bubble {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 15px;
    font-size: 14px;
    line-height: 1.4;
    word-break: break-word;
}

.user-message .message-bubble {
    background: #047404;
    color: white;
    border-bottom-right-radius: 5px;
}

.ai-message .message-bubble {
    background: #f0f0f0;
    color: #333;
    border-bottom-left-radius: 5px;
}

.chat-input-container {
    display: flex;
    gap: 8px;
    padding: 10px;
    background-color: rgba(248, 249, 250, 0.9);
    border-top: 1px solid rgba(222, 226, 230, 0.5);
    border-radius: 0 0 15px 15px;
}

.chat-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    outline: none;
    font-size: 14px;
    background: white;
}

.chat-input:focus {
    border-color: #056800;
}

.send-button {
    padding: 6px 12px;  /* 크기 줄임 */
    background: linear-gradient(45deg, #86da8a, #047404);
    color: white;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-weight: bold;
    font-size: 13px;    /* 폰트 크기 줄임 */
    transition: all 0.3s ease;
}

.send-button:hover {
    background: linear-gradient(45deg, #78c47c, #036203);
    transform: translateY(-1px);
}

.send-button:active {
    transform: translateY(0);
}

/* 스크롤바 스타일링 */
.chat-messages::-webkit-scrollbar {
    width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
    background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
}
</style>