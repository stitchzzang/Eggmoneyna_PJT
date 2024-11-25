<template>
    <div class="chatbot-container">
        <div class="chat-messages">
            <div v-for="message in messages" :key="message.id" 
                 :class="['message-wrapper', message.sender === 'user' ? 'user-message' : 'ai-message']">
                <div class="message-bubble" v-if="message.sender === 'user'">
                    {{ message.text }}
                </div>
                <div class="message-bubble markdown-body" v-else v-html="markdownToHtml(message.text)">
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
import OpenAI from 'openai';
import { marked } from 'marked';

export default {
    data() {
        return {
            userInput: '',
            messages: [],
            openai: null
        };
    },
    created() {
        this.openai = new OpenAI({
            apiKey: import.meta.env.VITE_OPENAI_API_KEY,
            dangerouslyAllowBrowser: true
        });
    },
    methods: {
        async sendMessage() {
            if (!this.userInput.trim()) return;
            
            this.addMessage('user', this.userInput);
            const userMessage = this.userInput;
            this.userInput = '';

            try {
                const aiResponse = await this.getAiResponse(userMessage);
                this.addMessage('ai', aiResponse);
            } catch (error) {
                console.error('Error:', error);
                this.addMessage('ai', '죄송합니다. 오류가 발생했습니다.');
            }
        },
        addMessage(sender, text) {
            if (!text) return;
            this.messages.push({
                id: Date.now(),
                sender,
                text
            });
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },
        scrollToBottom() {
            const chatMessages = document.querySelector('.chat-messages');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        },
        async getAiResponse(message) {
            try {
                const response = await this.openai.chat.completions.create({
                    model: "gpt-4o-mini",
                    messages: [
                    {"role": "system", "content": "You are a helpful assistant who explains financial topics simply and clearly for beginners."},
                    {"role": "user", "content": message}
                ],
                max_tokens: 1000,
                temperature: 0.7  // 간단하고 직관적인 답변을 유도
                });
                
                return response.choices[0].message.content.trim();
            } catch (error) {
                console.error('AI 응답 오류:', error);
                if (error.response?.status === 429) {
                    return '죄송합니다. 잠시 후 다시 시도해주세요.';
                }
                return `오류가 발생했습니다: ${error.message}`;
            }
        },
        markdownToHtml(text) {
            return marked(text);
        }
    },
    updated() {
        this.scrollToBottom();
    }
}
</script>

<style scoped>
.chatbot-container {
    position: fixed;
    bottom: 120px;
    right: 20px;
    width: 400px;
    height: 600px;
    background: rgba(255, 255, 255, 0.842);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    z-index: 1000;
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
    max-width: 75%;
    padding: 12px 18px;
    border-radius: 15px;
    font-size: 15px;
    line-height: 1.8;
    word-break: break-word;
    white-space: pre-line;
    text-align: left;
}

.user-message .message-bubble {
    background: #047404;
    color: white;
    border-bottom-right-radius: 5px;
}

.ai-message .message-bubble {
    background: #f8f9fa;
    padding: 15px 20px;
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
    font-size: 16px;
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
    font-size: 15px;    /* 폰트 크기 줄임 */
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

.markdown-body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

.markdown-body pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 13px;
    overflow: auto;
}

.markdown-body code {
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
    padding: 0.2em 0.4em;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}

.markdown-body p {
    margin-bottom: 13px;
}

.markdown-body ul, .markdown-body ol {
    padding-left: 2em;
    margin-bottom: 13px;
}
</style>