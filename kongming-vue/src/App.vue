<template>
  <div class="app-container">
    <div class="header">🪶 孔明军师</div>

    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, idx) in messages" :key="idx" class="msg" :class="msg.role">
        <div class="bubble">{{ msg.content }}</div>
      </div>

      <div v-if="loading" class="msg ai">
        <div class="bubble typing">孔明正在思考中...</div>
      </div>
    </div>

    <div class="input-bar">
      <input
        v-model="inputText"
        @keyup.enter="sendMessage"
        placeholder="请吩咐，主公..."
      />
      <button @click="sendMessage">策问</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const inputText = ref('')
const messages = ref([
  { role: 'ai', content: '主公，亮在此等候吩咐。' }
])
const loading = ref(false)
const chatBox = ref(null)

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text) return
  inputText.value = ''

  messages.value.push({ role: 'user', content: text })
  loading.value = true

  await nextTick()
  chatBox.value.scrollTop = chatBox.value.scrollHeight

  try {
    const res = await axios.post('http://127.0.0.1:8000/chat', {
      question: text
    })
    messages.value.push({ role: 'ai', content: res.data.answer })
  } catch (e) {
    messages.value.push({ role: 'ai', content: '主公，今日信号不畅，稍后再试。' })
  }

  loading.value = false
  await nextTick()
  chatBox.value.scrollTop = chatBox.value.scrollHeight
}
</script>

<style scoped>
.app-container {
  max-width: 700px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0b121e;
  color: #e3c382;
}

.header {
  padding: 16px;
  text-align: center;
  font-size: 20px;
  border-bottom: 1px solid #253144;
}

.chat-box {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.msg {
  display: flex;
}

.msg.user {
  justify-content: flex-end;
}

.msg.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 14px;
  line-height: 1.6;
}

.user .bubble {
  background: #3b5779;
  color: white;
  border-bottom-right-radius: 4px;
}

.ai .bubble {
  background: #1b283a;
  color: #e3c382;
  border-bottom-left-radius: 4px;
}

.typing {
  color: #a08652;
}

.input-bar {
  display: flex;
  padding: 16px;
  gap: 10px;
  border-top: 1px solid #253144;
}

input {
  flex: 1;
  padding: 14px 16px;
  border-radius: 12px;
  border: none;
  background: #151e2d;
  color: #e3c382;
  font-size: 16px;
}

button {
  padding: 14px 20px;
  border-radius: 12px;
  background: #c89a56;
  color: #111;
  font-weight: bold;
  border: none;
  cursor: pointer;
}
</style>