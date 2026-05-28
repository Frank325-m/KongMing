
<template>
  <div class="chat-main">
    <div class="chat-header">
      <button class="menu-toggle" @click="$emit('toggle-sidebar')">☰</button>
      <span class="title">{{ currentSessionTitle || '孔明军师 - 专属谋断' }}</span>
      <div class="header-right">
        <button class="wisdom-bag-toggle" @click="$emit('open-wisdom-bag')">
          <span class="wisdom-icon">📜</span> 锦囊
        </button>
      </div>
    </div>

    <div class="user-info-bar" v-if="userType">
      <div class="user-info-left">
        <span class="user-avatar">{{ userType === 'user' ? '👤' : '🚶' }}</span>
        <div class="user-details">
          <span class="user-name">{{ userType === 'user' ? userEmail : '访客' }}</span>
          <span class="user-type">{{ userType === 'user' ? '登录用户' : '访客模式' }}</span>
        </div>
      </div>
      <div class="quota-info">
        <span class="quota-text">今日剩余</span>
        <span class="quota-count" :class="{ low: remainingQuota <= 2 }">{{ remainingQuota }}</span>
        <span class="quota-total">/ {{ todayLimit }}</span>
      </div>
      <button class="logout-btn" v-if="userType === 'user'" @click="$emit('logout')">
        辞别离去
      </button>
      <button class="login-btn" v-else @click="$emit('open-login-modal')">
        登堂入室
      </button>
    </div>

    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, idx) in messages" :key="idx" class="msg" :class="msg.role">
        <div class="bubble" v-if="msg.role === 'ai'">
          {{ msg.content }}
          <button
            v-if="msg.content && !loading"
            class="collect-btn"
            @click="collectWisdom(msg.content)"
            title="收录锦囊"
          >
            💾 收录锦囊
          </button>
        </div>
        <div class="bubble" v-else>
          {{ msg.content }}
        </div>
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
        呈上问策
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'

const props = defineProps({
  messages: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  sidebarCollapsed: { type: Boolean, default: false },
  currentSessionTitle: { type: String, default: '' },
  remainingQuota: { type: Number, default: 5 },
  userType: { type: String, default: 'guest' },
  userEmail: { type: String, default: '' },
  todayLimit: { type: Number, default: 5 }
})

const emit = defineEmits(['send-message', 'toggle-sidebar', 'open-wisdom-bag', 'collect-wisdom', 'logout', 'open-login-modal'])

const chatBox = ref(null)
const inputText = ref('')

const currentQuestion = computed(() => {
  const userMessages = props.messages.filter(m => m.role === 'user')
  return userMessages.length > 0 ? userMessages[userMessages.length - 1].content : ''
})

const handleSend = () => {
  if (inputText.value.trim()) {
    emit('send-message', inputText.value.trim())
    inputText.value = ''
  }
}

const collectWisdom = (content) => {
  console.log('🤖 collectWisdom called, title:', currentQuestion.value, 'content length:', content.length)
  const title = currentQuestion.value || '孔明妙计'
  emit('collect-wisdom', title, content)
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

watch(() => props.messages.length, async () => {
  await nextTick()
  scrollToBottom()
})

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

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.wisdom-bag-toggle {
  padding: 8px 16px;
  border: 1px solid #d4b878;
  background: linear-gradient(135deg, rgba(212, 184, 120, 0.1), transparent);
  color: #d4b878;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.wisdom-bag-toggle:hover {
  background: linear-gradient(135deg, rgba(212, 184, 120, 0.2), transparent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.3);
}

.wisdom-icon {
  font-size: 16px;
}

.user-info-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background-color: #121b2b;
  border-bottom: 1px solid #283447;
}

.user-info-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  font-size: 32px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  color: #e6c88c;
  font-size: 14px;
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-type {
  color: #64748b;
  font-size: 12px;
}

.quota-info {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(61, 90, 76, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #3d5a4c;
}

.quota-text {
  color: #94a3b8;
  font-size: 13px;
}

.quota-count {
  color: #e6c88c;
  font-size: 20px;
  font-weight: 700;
}

.quota-count.low {
  color: #ef4444;
}

.quota-total {
  color: #64748b;
  font-size: 14px;
}

.logout-btn {
  padding: 8px 16px;
  border: 1px solid #475569;
  background: transparent;
  color: #94a3b8;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.login-btn {
  padding: 8px 16px;
  border: 2px solid #d4b878;
  background: linear-gradient(180deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.3);
}

.chat-box {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  position: relative;
}

.msg.ai .bubble {
  padding-bottom: 40px;
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

.collect-btn {
  position: absolute;
  bottom: 8px;
  right: 12px;
  padding: 4px 10px;
  border: 1px solid rgba(212, 184, 120, 0.3);
  background: rgba(212, 184, 120, 0.1);
  color: #d4b878;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 4px;
  z-index: 10;
}

.msg.ai:hover .collect-btn {
  opacity: 1;
}

.collect-btn:hover {
  background: rgba(212, 184, 120, 0.2);
  border-color: #d4b878;
  transform: translateY(-1px);
}

.collect-btn:active {
  transform: scale(0.95);
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
  border: 2px solid #334155;
  background-color: #1e293b;
  color: #e2e8f0;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
}

.input-bar input:focus {
  border-color: #d4b878;
  background-color: #27344a;
  box-shadow: 0 0 0 3px rgba(212, 184, 120, 0.15);
}

.input-bar input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-bar button {
  padding: 14px 28px;
  border: 2px solid #d4b878;
  background: linear-gradient(135deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-radius: 10px;
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

  .user-info-bar {
    padding: 10px 16px;
    flex-wrap: wrap;
    gap: 10px;
  }

  .quota-info {
    padding: 6px 12px;
  }

  .user-name {
    max-width: 120px;
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
