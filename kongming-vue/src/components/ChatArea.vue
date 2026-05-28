
<template>
  <div class="chat-main">
    <div class="chat-header">
      <button class="menu-toggle" @click="$emit('toggle-sidebar')">☰</button>
      <span class="title">{{ currentSessionTitle || '孔明军师 - 专属谋断' }}</span>
    </div>

    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, idx) in messages" :key="idx" class="msg" :class="msg.role">
        <div class="bubble">{{ msg.content }}</div>
      </div>

      <div v-if="loading" class="msg ai">
        <div class="bubble loading-wrap">
          <span class="fan-icon">🪶</span>
          <span class="loading-text">孔明推演局势中...</span>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <input
        v-model="inputText"
        @keyup.enter="handleSend"
        placeholder="请主公吩咐，亮即刻推演..."
        :disabled="loading"
      />
      <button @click="handleSend" :class="{ disabled: loading }">
        献策问策
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  messages: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  sidebarCollapsed: { type: Boolean, default: false },
  currentSessionTitle: { type: String, default: '' }
})

const emit = defineEmits(['send-message', 'toggle-sidebar'])

const chatBox = ref(null)
const inputText = ref('')

const handleSend = () => {
  if (inputText.value.trim()) {
    emit('send-message', inputText.value.trim())
    inputText.value = ''
  }
}

const scrollToBottom = () => {
  if (chatBox.value) {
    nextTick(() => {
      if (chatBox.value) {
        chatBox.value.scrollTop = chatBox.value.scrollHeight
        const lastMsg = chatBox.value.lastElementChild
        if (lastMsg) {
          lastMsg.scrollIntoView({ behavior: 'smooth', block: 'end' })
        }
        setTimeout(() => {
          if (chatBox.value) {
            chatBox.value.scrollTop = chatBox.value.scrollHeight
          }
        }, 100)
      }
    })
  }
}

// 监听消息长度变化时滚动
watch(() => props.messages.length, async () => {
  await nextTick()
  scrollToBottom()
})

// 监听最后一条消息内容变化时滚动
watch(
  () => props.messages[props.messages.length - 1]?.content,
  async () => {
    await nextTick()
    scrollToBottom()
  },
  { deep: true }
)
</script>

<style scoped>
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #0f172a;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid #1e293b;
  background-color: #0f172a;
}

.menu-toggle {
  display: none;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
}

.title {
  font-size: 18px;
  font-weight: 500;
  color: #d4b878;
  letter-spacing: 1px;
}

.chat-box {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  /* 自定义滚动条 - WebKit 浏览器 */
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

.chat-box:hover {
  scrollbar-color: #475569 transparent;
}

.chat-box::-webkit-scrollbar {
  width: 6px;
}

.chat-box::-webkit-scrollbar-track {
  background: transparent;
}

.chat-box::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

.chat-box:hover::-webkit-scrollbar-thumb {
  background-color: #475569;
}

.chat-box:active::-webkit-scrollbar-thumb {
  background-color: #64748b;
}

.msg {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.msg.user {
  flex-direction: row-reverse;
}

.bubble {
  max-width: 70%;
  padding: 14px 18px;
  border-radius: 16px;
  line-height: 1.8;
  font-size: 15px;
  box-sizing: border-box;
  text-align: left;
}

.user .bubble {
  background-color: #2a3b55;
  color: #f0e6d2;
  border-bottom-right-radius: 4px;
}

.ai .bubble {
  background-color: #121b2b;
  color: #e6c88c;
  border: 1px solid #283447;
  border-bottom-left-radius: 4px;
}

.loading-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.fan-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #a1a1aa;
}

.input-bar {
  padding: 20px 24px;
  border-top: 1px solid #1e293b;
  display: flex;
  gap: 16px;
  background-color: #0f172a;
}

.input-bar input {
  flex: 1;
  padding: 14px 20px;
  border: 1px solid #334155;
  background-color: #1e293b;
  color: #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
}

.input-bar input:focus {
  border-color: #4a6b5a;
  background-color: #27344a;
}

.input-bar input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-bar button {
  padding: 14px 28px;
  border: none;
  background: linear-gradient(135deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.input-bar button:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(61, 90, 76, 0.4);
}

.input-bar button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .chat-box {
    padding: 16px;
  }

  .bubble {
    max-width: 85%;
    font-size: 14px;
  }

  .input-bar {
    padding: 16px;
  }
}
</style>
